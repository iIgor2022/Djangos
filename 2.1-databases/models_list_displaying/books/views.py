from datetime import datetime

from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_pagi(request, dt: datetime):
    template = 'books/books_list.html'
    book = Book.objects.filter(pub_date=dt.date())
    next_page = Book.objects.filter(pub_date__gt=dt.date()).first()
    prev_page = Book.objects.filter(pub_date__lt=dt.date()).first()
    context = {
        'books': book,
        "prev_page": prev_page,
        "next_page": next_page,
    }
    return render(request, template, context)
