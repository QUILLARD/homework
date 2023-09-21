from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from precise_bbcode.fields import BBCodeTextField


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')


class RubricManager(models.Manager):
    def get_queryset(self):
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        return self.get_queryset().order_by_bb_count()


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


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
    objects = RubricManager()

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
    objects = models.Manager()
    by_price = BbManager()

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


class Customers(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.IntegerField(verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город')


class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    content = models.TextField(verbose_name='О себе')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def get_absolute_url(self):
        return reverse('visits', kwargs={'st_id': self.pk})


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    students = models.ManyToManyField('Student', through='Kit', through_fields=('course', 'student'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Kit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    visits = models.IntegerField(verbose_name='Количество посещений')

    def __str__(self):
        return f'{self.course.name} - {self.student.first_name} {self.student.last_name}'

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        abstract = True


class Authors(TimeStampedModel):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Books(TimeStampedModel):
    author = models.OneToOneField(Authors, on_delete=models.CASCADE, verbose_name='Автор')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reviews(TimeStampedModel):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reviews', verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Рецензия')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'Рецензия - "{self.book.name}" от {self.user.username}'

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензия'

# Домашняя работа 34
class Article(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = BBCodeTextField(verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
