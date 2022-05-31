from django.db import models


class AdminModel(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    username = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'admin'


    @staticmethod
    def isExist():
        pass