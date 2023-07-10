from django import forms
from tasksheet.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

