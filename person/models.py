from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    name = models.CharField("Name", max_length=255)
    cpf = models.CharField("CPF", max_length=11, unique=True)
    birthday = models.DateField("Birthday", auto_now=False, auto_now_add=False)
    user = models.OneToOneField(User, related_name="person", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.name

    def get_by_cpf(self, cpf):
        return Person.objects.filter(cpf=cpf)