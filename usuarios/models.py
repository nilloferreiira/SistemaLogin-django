from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    rua = CharField(max_length=100, blank=True, null=True)
    numero = CharField(max_length=1000, blank=True, null=True)
    cep = CharField(max_length=8)