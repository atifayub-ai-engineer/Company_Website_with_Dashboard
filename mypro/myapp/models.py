import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()

    def __str__(self):
        return self.email


class Customer(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    address = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Extended(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)


@receiver(pre_delete, sender=User)
def remove_pic(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.img.path)
    except:
        pass


