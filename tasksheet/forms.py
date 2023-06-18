from django.forms import ModelForm
from tasksheet.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'notes')
