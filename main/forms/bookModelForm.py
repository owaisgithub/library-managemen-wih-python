from django import forms

from ..models.bookModel import BookModel


class BookModelForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'