function sendInterest(userId) {
    fetch(`/api/interests/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ receiver: userId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            alert('Interest sent successfully.');
        } else {
            alert('Error sending interest.');
        }
    });
}

function acceptInterest(interestId) {
    fetch(`/api/interests/${interestId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ accepted: true })
    })
    .then(response => response.json())
    .then(data => {
        if (data.accepted) {
            alert('Interest accepted.');
            location.reload();
        } else {
            alert('Error accepting interest.');
        }
    });
}

function rejectInterest(interestId) {
    fetch(`/api/interests/${interestId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ rejected: true })
    })
    .then(response => response.json())
    .then(data => {
        if (data.rejected) {
            alert('Interest rejected.');
            location.reload();
        } else {
            alert('Error rejecting interest.');
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const chatForm = document.querySelector('#chat-form');
    if (chatForm) {
        const roomName = chatForm.getAttribute('data-room-name');
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').innerHTML += (
                '<div><b>' + data.sender + ':</b> ' + data.message + '</div>'
            );
        };

        chatForm.onsubmit = function(e) {
            e.preventDefault();
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    }
});
