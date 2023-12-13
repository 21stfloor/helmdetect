Install vscode


Web
Python 3.9.13 - Programming language  https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
Checkbox should be checked for Add Python to PATH

Download and install XAMPP https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.0/xampp-windows-x64-8.2.0-0-VS16-installer.exe


Use Command Prompt:
Setup Web Source code
python --version //To check if the python was properly installed
python -m venv venv //Creates a virtual environment folder,

In vscode press Ctrl+Shift+P
Select Interpreter
Select venv python 3.9.13
re-open cmd


pip install -r requirements.txt //this will install all dependencies

Open xampp 
Start Mysql and Apache
Click Mysql -> Admin
In Browser, Click New (to create a database)
type in database name : helmetdetect$database
then Click create

In windows start menu type in: environment variables
Click Environment variables
Under System Variables add new
Variable name : DJANGO_ENV
Variable value : LOCAL

Cmd

python manage.py makemigrations //creates a mapping of python classes into database
python manage.py migrate // this will perform the actual conversion of python classes into mysql database




python manage.py runserver //This will run the web app




To save a backup json file(optional):
python manage.py dumpdata app admin_interface.theme --indent=2 > backup.json