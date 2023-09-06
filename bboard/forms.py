from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from bboard.models import Bb, IceCream


class BbForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubric'].empty_label = 'Рубрика не выбрана'

    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст!'})

    class Meta:
        model = Bb
        fields = ('title', 'slug', 'content', 'image', 'price', 'rubric')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 35, 'rows': 5, 'style': 'margin-top: 6px;'}),
            'price': forms.TextInput(attrs={'class': 'form-input'}),
            'rubric': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ('name', 'description', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 35, 'rows': 5, 'style': 'margin-top: 20px;'}),
        }


class UserCheckForm(forms.Form):
    name = forms.CharField(max_length=10, label='Имя')
    age = forms.IntegerField(label='Возраст')


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=20, label='Имя')
    email = forms.EmailField(label='Почта')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label='Описание')
    captcha = CaptchaField(label='Введите текс с картинки')
