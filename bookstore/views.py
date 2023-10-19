from django.db.models import Q
from django.shortcuts import render
from django.views import View

from .models import *


class BookView(View):
    template_name = 'bookstore/index.html'

    def get(self, request):
        search_query = self.request.GET.get('search')
        status = False
        if search_query:
            books = Book.objects.filter(
                Q(book_name__icontains=search_query)
            )
            status = True
        else:
            books = Book.objects.all()

        search_count = len(books)
        context = {
            'title': 'Список учащихся',
            'books': books,
            'search_count': search_count,
            'search_query': search_query,
            'status': status
        }
        return render(request, self.template_name, context)
