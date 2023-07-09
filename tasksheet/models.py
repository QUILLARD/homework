from django.db import models


class Task(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Задача'
    )

    notes = models.CharField(
        max_length=100,
        verbose_name='Заметки'
    )

    start = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало'
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Лист задач'
        verbose_name_plural = 'Лист задач'
        ordering = ['start']

