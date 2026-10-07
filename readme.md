Ticket Reservation and Scanning System

A backend system using Django and Django REST framework for a simple event ticket reservation platform. Users should be able to view an event, reserve tickets, receive a unique ticket, and have that ticket scanned at the event entrance. 

Running the project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Run the tests with
python manage.py test api


Future Improvements
Use Postgresql as the main db
add idempotency key 
add logging 
add API throttling 
add docker
add swagger/openAPI