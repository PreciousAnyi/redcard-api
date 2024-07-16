from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomManager(BaseUserManager):
    def create_user(self, personnel_no, fullname, password=None):
        if not personnel_no:
            raise ValueError("The personnel number field is required")
        if not fullname:
            raise ValueError("The fullname field is required")

        if self.model.objects.filter(personnel_no=personnel_no).exists():
            raise ValueError("A user with this personnel number already exists")

        user = self.model(personnel_no=personnel_no, fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, personnel_no, fullname, password=None):
        user = self.create_user(personnel_no, fullname, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    personnel_no = models.CharField(primary_key= True, max_length=50)
    fullname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomManager()

    USERNAME_FIELD = 'personnel_no'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.personnel_no
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Invigilator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    threshold = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f"{self.user.fullname} - {self.threshold}"



