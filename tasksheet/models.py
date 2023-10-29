from django.db import models
from django.urls import reverse


class Task(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Задача'
    )

    notes = models.CharField(
        max_length=255,
        verbose_name='Описание'
    )

    start = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало'
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name='Статус'
    )

    def get_absolute_url(self):
        return reverse('tasksheet:update_task', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Лист задач'
        verbose_name_plural = 'Лист задач'
        ordering = ['start']
