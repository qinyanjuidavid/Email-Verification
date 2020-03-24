from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser



class custommanager(BaseUserManager):
    def create_user(self,email,username,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have an email.')
        if not password:
            raise ValueError('Users must have a password.')
        if not username:
            raise ValueError('Users must have a username.')
        user_obj=self.model(
        email=self.normalize_email(email),
        username=username
        )
        user_obj.set_password(password)
        user_obj.is_active=is_active
        user_obj.is_admin=is_admin
        user_obj.is_staff=is_staff
        user_obj.save(using=self._db)
        return user_obj
    def create_staff(self,email,username,password=None):
        user=self.create_user(
        email,
        username,
        password=password,
        is_staff=True,
        is_active=True,

        )
        return user
    def create_superuser(self,email,username,password=None):
        user=self.create_user(
        email,
        username,
        password=password,
        is_admin=True,
        is_active=True,
        is_staff=True
        )
        return user
class User(AbstractBaseUser):
    username=models.CharField(max_length=255,verbose_name="Username",unique=True)
    first_name=models.CharField(max_length=256)
    last_name=models.CharField(max_length=256)
    email=models.EmailField(verbose_name="Email Address",max_length=255,unique=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=custommanager()


    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def staff(self):
        return self.staff
    @property
    def active(self):
        return self.active
    @property
    def admin(self):
        return self.admin

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
