from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    address = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=11, null=False, blank=False, unique=True)

    objects = CustomUserManager()


class Profile(models.Model):
    image = models.ImageField(upload_to='profiles/images/', default='profiles/images/default-user.jpg')
    user  = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username} profile'

class Item(models.Model):
    name  = models.CharField(max_length=255)
    price = models.FloatField(max_length=6)
    code  = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    image = models.ImageField(upload_to='items/images/%y/%m/%d/%H/%M/%S', default='items/images/default.jpg')
    def __str__(self) -> str:
        return f'{self.name}'


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username} add this item {self.item.name} to Cart'
    
class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return 'Order of ' +self.user.username
