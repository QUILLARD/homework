from django.contrib.auth.models import User
from django.db import models


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
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class Bb(models.Model):
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']


class Parent(models.Model):
    floors = [
        ('m', 'man'),
        ('w', 'woman'),
    ]

    name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        blank=False,
    )

    floor = models.CharField(
        max_length=1,
        choices=floors,
        default='m',
    )

    years = models.PositiveSmallIntegerField(
        verbose_name='Лет',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'
        ordering = ['name']


class Child(models.Model):
    name_child = models.CharField(
        max_length=20,
        verbose_name='Имя',
        blank=False,
    )

    years_child = models.PositiveSmallIntegerField(
        verbose_name='Лет',
    )

    parent = models.ForeignKey(
        'Parent',
        on_delete=models.PROTECT,
        verbose_name='Родитель',
    )

    def __str__(self):
        return self.name_child

    class Meta:
        verbose_name = 'Ребенок'
        verbose_name_plural = 'Дети'
        ordering = ['name_child']


class IceCream(models.Model):
    taste = models.CharField(
        max_length=20,
        verbose_name='Вкус',
    )
    markets = models.ManyToManyField(
        'IceCreamMarket',
    )

    def __str__(self):
        return self.taste

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'
        ordering = ['taste']


class IceCreamMarket(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Название',
    )

    address = models.CharField(
        max_length=30,
        verbose_name='Адрес',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Киоск'
        verbose_name_plural = 'Киоски'
        ordering = ['name']
