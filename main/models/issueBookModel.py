from operator import mod
from django.db import models

from datetime import date, timedelta

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


    @staticmethod
    def get_all():
        issues = IssueBookModel.objects.all()
        return issues


    @staticmethod
    def today_issue_books_no():
        td = IssueBookModel.objects.filter(issue_date = date.today())
        no = len(td)
        return no


    def issue_book(bookId, studentId):
        issueDate = date.today()
        returnDate = issueDate + timedelta(days=15)
        book = IssueBookModel.objects.create(
                                            student_id = studentId,
                                            book_id = bookId,
                                            issue_date = issueDate,
                                            return_date = returnDate
                                            )

        return book