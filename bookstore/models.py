from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        abstract = True


class Author(TimeStampedModel):
    author_first_name = models.CharField(max_length=255, verbose_name='Имя')
    author_last_name = models.CharField(max_length=255, verbose_name='Фамилия')

    def __str__(self):
        return f'{self.author_first_name} {self.author_last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Genre(TimeStampedModel):
    genre_name = models.CharField(max_length=255, verbose_name='Жанр')

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(TimeStampedModel):
    book_author = models.OneToOneField('Author', on_delete=models.PROTECT, verbose_name='Автор')
    book_name = models.CharField(max_length=255, verbose_name='Наименование')
    book_genre = models.ForeignKey('Genre', on_delete=models.PROTECT)
    book_description = models.TextField(verbose_name='Описание')
    book_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    book_vendor_code = models.PositiveBigIntegerField()

    def __str__(self):
        return self.book_name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Review(TimeStampedModel):
    review_book = models.ForeignKey('Book', on_delete=models.PROTECT, related_name='reviews', verbose_name='Книга')
    review_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    review_text = models.TextField(verbose_name='Рецензия')
    review_rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'Рецензия - "{self.review_book.name}" от {self.review_user.username}' # Будет ошибка из-за имени

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензия'
