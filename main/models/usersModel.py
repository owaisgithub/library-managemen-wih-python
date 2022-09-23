from django.db import models

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an Username')
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, username, password, **extra_fields):
        # user = self._create_user(email, password, **extra_fields)
        extra_fields.setdefault('is_student', True)
        #extra_fields.setdefault('is_staff', True)
        # user.save(using=self._db)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an Username')
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
        #return self._create_user(username, password, **extra_fields)


class UsersModel(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    password = models.CharField(max_length=255, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
