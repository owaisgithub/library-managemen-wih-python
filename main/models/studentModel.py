from django.db import models

from django.contrib.auth.hashers import make_password

from .usersModel import UsersModel



class StudentModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    student = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=30, unique=True, null=False)
    mobile_no = models.CharField(max_length=15, null=False)
    address = models.CharField(max_length=255)
    course = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='student-images/')
    fine = models.FloatField(default=0)
    tag = models.CharField(max_length=30, default='none')

    class Meta:
        db_table = 'student'



    #@staticmethod
    def save_student(sid, sname, semail, smobile, saddress, scourse, simage):
        student = StudentModel.objects.create(
                                        student_id = sid,
                                        name = sname, email = semail, 
                                        mobile_no = smobile, address = saddress, 
                                        course = scourse, image = simage
                                        )
        return student

    # @staticmethod
    def blacklisted_student_no():
        student = StudentModel.objects.filter(tag = 'blacklisted')
        return len(student)

    def active_student_no():
        student = StudentModel.objects.filter(tag = 'active')
        return len(student)

    def cancelled_student_no():
        student = StudentModel.objects.filter(tag = 'cancelled')
        return len(student)

    def requested_student():
        student = StudentModel.objects.filter(tag = 'none')
        return student

    def get_all_active():
        student = StudentModel.objects.filter(tag = 'active')
        return student

    def get_all_blacklisted():
        student = StudentModel.objects.filter(tag = 'blacklisted')
        return student

    def get_all_cancelled():
        student = StudentModel.objects.filter(tag = 'cancelled')
        return student


