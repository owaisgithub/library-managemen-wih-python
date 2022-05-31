from django.urls import path

from .views import homeViews, bookViews, studentViews, adminViews

urlpatterns = [
    path('', homeViews.homepage, name='home'),
    path('admin-panel/', adminViews.admin_panel),
    path('add-book', bookViews.add_book, name='add_book'),
    path('student-registration/', studentViews.student_registration)
]