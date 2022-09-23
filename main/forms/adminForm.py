from django import forms

from ..models.usersModel import UsersModel


class AdminForm(forms.ModelForm):
    class Meta:
        model = UsersModel
        fields = '__all__'