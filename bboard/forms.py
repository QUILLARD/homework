from django import forms
from django.core.exceptions import ValidationError

from bboard.models import Bb


class BbForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubric'].empty_label = 'Рубрика не выбрана'

    class Meta:
        model = Bb
        fields = ('title', 'slug', 'content', 'image', 'price', 'rubric')
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

