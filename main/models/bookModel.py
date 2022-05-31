from turtle import st
from django.db import models


class BookModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn_no = models.CharField(max_length=20)
    publication = models.CharField(max_length=50)
    edition = models.CharField(max_length=20)
    rack_no = models.CharField(max_length=10)
    no_of_copy = models.IntegerField(default=0)
    image = models.ImageField(upload_to='books-images')

    class Meta:
        db_table = 'books'

    @staticmethod
    def all_books():
        books = BookModel.objects.all()

    @staticmethod
    def book_by_tag(key):
        books = None
        if BookModel.objects.filter(title = key).exists():
            books = BookModel.objects.filter(title = key)

        elif BookModel.objects.filter(author = key).exists():
            books = BookModel.objects.filter(author = key)
            
        elif BookModel.objects.filter(publication = key).exists():
            books = BookModel.objects.filter(publication = key)
        else:
            books = None

        return books