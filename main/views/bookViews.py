from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.db.models import Q

from django.contrib import messages

from ..models.bookModel import BookModel

from ..forms.bookModelForm import BookModelForm


def add_book(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            forms = BookModelForm(request.POST, request.FILES)
            if forms.is_valid():
                forms.save()
                messages.info(request, "Book Added Succesfully!")
                return render(request, 'admin_panel/add_book.html', {'forms': forms})

        else:
            forms = BookModelForm()
        return render(request, 'admin_panel/add_book.html', {'forms':forms})
    else:
        return HttpResponse('Failed')

def get_books(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            query = request.POST.get('search')

            if query is not None:
                lookups = Q(title__icontains=query) | Q(author__icontains=query) | Q(publication__icontains=query)
                books = BookModel.objects.filter(lookups)
                context = {
                    'books': books,
                    'query': query
                }

                return render(request, 'admin_panel/view_books.html', context)

        else:
            books = BookModel.all_books()
            context = {
                'books' : books
            }
            return render(request, 'admin_panel/view_books.html', context)
    else:
        return HttpResponse("User not logged in")

def update_book(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        book = BookModel.objects.get(id = id)

        forms = BookModelForm(request.POST or None, instance = book)

        if forms.is_valid():
            forms.save()
            return redirect('/show-books')

        context = {
            'forms':forms
        }

        return render(request, 'update_view.html', context)
    else:
        return HttpResponse("User is not logged in")


def delete_view(request, id):
    if request.user.is_authenticated and request.user.is_admin:
        book = BookModel.objects.get(id = id)

        if request.method == 'POST':
            book.delete()
            return redirect('/show-books')

        return render(request, 'admin_panel/delete_view.html')
    else:
        return HttpResponse("User is not logged in")