from operator import mod
from django.db import models

#from datetime import date, timedelta

from .studentModel import StudentModel

from .bookModel import BookModel

class IssueBookModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()

    class Meta:
        db_table = 'issue_book'