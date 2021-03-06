from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Category(models.Model):
    name = models.CharField(default="", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Friend(models.Model):
    name = models.CharField(default="", max_length=20)
    furigana = models.CharField(blank=True, null=True, max_length=20)
    nickname = models.CharField(blank=True, null=True, max_length=20)
    sex = models.IntegerField(default=0)
    birthday = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    birthplace = models.CharField(blank=True, null=True, max_length=30)
    hobby = models.CharField(blank=True, null=True, max_length=30)
    company = models.CharField(blank=True, null=True, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

class Memo(models.Model):
    text = models.CharField(default="", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_category(sender, **kwargs):
    if kwargs['created']:
        default_category = Category.objects.create(user=kwargs['instance'])
        default_category.name = "???????????????"
        default_category.save()
