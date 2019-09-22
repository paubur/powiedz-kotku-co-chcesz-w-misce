from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Cat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    age = models.IntegerField()
    birthmark = models.CharField(max_length=255)
    medical_condition = models.TextField()
    diet = models.BooleanField(default=False, blank=True)
    diet_description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['user', 'name']


class Food(models.Model):
    cat = models.ManyToManyField(Cat)
    company = models.CharField(max_length=64)
    name = models.CharField(max_length=255)

# class Food(models.Model):
#     cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
#     company = models.CharField(max_length=64)
#     name = models.CharField(max_length=255)


class Composition(models.Model):
    food = models.ManyToManyField(Food, through="Content")
    name = models.CharField(max_length=64)


class Content(models.Model):
    quantity = models.IntegerField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)




