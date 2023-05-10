import os
from create_django_project import NAME_PROJECT

os.chdir(NAME_PROJECT)

os.system(f"python manage.py runserver")
