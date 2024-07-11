# interest-chat-app

How to setup the project:

Clone the Repository:

    git clone https://github.com/Kumar-Priyesh/interest-chat-app.git
    cd project_directory

Backend Setup:

    python -m venv venv
    
    source venv/bin/activate - for mac/linux
    venv\Scripts\activate -for windows
    
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

All the prerequisites and dependencies are there in requirements.txt and will be installed once above command is run. When 'python manage.py runserver' cmd executed, the application will be live.

Access the Application: Open http://localhost:8000 in web browser to view the application.
