from django.shortcuts import render

from ..models.bookModel import BookModel

from ..forms.bookModelForm import BookModelForm


def add_book(request):
    if request.method == 'POST':
        form = BookModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            #img_obj = form.instance
            return render(request, 'admin_panel/add_book.html', {'form': form})

    else:
        form = BookModelForm()

    return render(request, 'admin_panel/add_book.html', {'form':form})

def get_books(request):
    books = BooModel.all_book()
    context = {
        'books' : books
    }
    return render(request, 'admin_panel/view_books.html', context)

def update_book(request, id):
    book = BookModel.objects.get(id = id)

    form = BookModelForm(request.POST, request.FIELS, instance = book)

    if form.is_valid():
        form.save()