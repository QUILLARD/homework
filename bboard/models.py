from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


def get_positive_numbers(num):
    if num < 0:
        raise ValidationError('Число %(value)s меньше нуля', code='odd', params={'value': num})


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


class Spare(models.Model):
    name = models.CharField(
        max_length=30,
    )


class Machine(models.Model):
    name = models.CharField(
        max_length=30,
    )

    spares = models.ManyToManyField(
        Spare,
    )


class Rubric(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('by_rubric', kwargs={'rubric_slug': self.slug})


class Bb(models.Model):
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=255, verbose_name="Заголовок объявления")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение')
    content = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    time_create = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-time_create', 'title']

    def get_absolute_url(self):
        return reverse('bb_detail', kwargs={'bb_slug': self.slug})


class IceCream(models.Model):
    name = models.CharField(max_length=60, db_index=True, verbose_name='Наименование')
    description = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'

