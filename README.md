## Project Setup
1. Install dependencies:
pip install -r requirements.txt
Reset database:
python manage.py reset_database
Create superuser:
python manage.py createsuperuser
Run server:
python manage.py runserver
#-----------------------------------
In case of error:
If you see no such table error, run the following command (reset_database).
python manage.py reset_database

Create the requirements.txt file with the following command:
pip freeze > requirements.txt
Test and continue
After fixing the problem:

Run the following commands:
python manage.py reset_database
python manage.py createsuperuser
python manage.py runserver
Go to the following addresses and check if they work:
http://127.0.0.1:8000/ (Entity List)
http://127.0.0.1:8000/admin/ (Admin Interface)
Add an entity and a sample field via the UI or Admin.