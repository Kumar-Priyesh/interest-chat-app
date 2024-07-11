from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets, permissions
from .forms import UserRegistrationForm, UserLoginForm
from .models import Interest, Message
from .serializers import InterestSerializer, MessageSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index_view(request):
    return render(request, 'index.html')

@login_required
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    sent_requests = Interest.objects.filter(sender=request.user, accepted=False).values_list('receiver_id', flat=True)
    return render(request, 'user_list.html', {'users': users, 'sent_requests': sent_requests})

@login_required
def received_interests_view(request):
    received_interests = Interest.objects.filter(receiver=request.user, accepted=False)
    return render(request, 'received_interests.html', {'received_interests': received_interests})

@login_required
def accept_interest_view(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    interest.accepted = True
    interest.save()
    return redirect('chat', interest_id=interest.id)


@login_required
def send_request_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    interest, created = Interest.objects.get_or_create(sender=request.user, receiver=receiver, accepted=False)
    if created:
        # Optionally add a message to indicate the request was sent successfully
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def send_message_view(request, interest_id):
    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        interest = get_object_or_404(Interest, id=interest_id)
        sender = request.user
        receiver = interest.receiver if interest.sender == sender else interest.sender
        message = Message.objects.create(sender=sender, receiver=receiver, content=message_content)

        # Render the message partial template
        message_html = render_to_string('message_partial.html', {'message': message})
        return HttpResponse(message_html)

    return redirect('chat', interest_id=interest_id)

@login_required
def chat_list_view(request):
    interests = Interest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user), 
        accepted=True
    )
    chats = []
    for interest in interests:
        other_user = interest.sender if interest.sender != request.user else interest.receiver
        chats.append({
            'interest': interest,
            'other_user': other_user
        })
    return render(request, 'chat_list.html', {'chats': chats})

@login_required
def chat_view(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    other_user = interest.sender if interest.sender != request.user else interest.receiver
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Create a room name based on the users' ids
    room_name = f'chat_{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}'
    
    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages,
        'interest': interest,
        'room_name': room_name  # Pass the room name to the template
    })

def chat_room(request, room_id):
    receiver = get_object_or_404(User, id=room_id)
    return render(request, 'chat.html', {
        'receiver': receiver
    })


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        receiver = User.objects.get(id=receiver_id)
        serializer.save(sender=self.request.user, receiver=receiver)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        receiver = User.objects.get(id=receiver_id)
        serializer.save(sender=self.request.user, receiver=receiver)
