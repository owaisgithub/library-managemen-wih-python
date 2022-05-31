from django.db import models


class StudentModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=30, unique=True, null=False)
    mobile_no = models.CharField(max_length=15, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255)
    couse = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='student-images/')
    fine = models.FloatField(default=0)
    tag = models.CharField(max_length=15, default='none')

    class Meta:
        db_table = 'student'
