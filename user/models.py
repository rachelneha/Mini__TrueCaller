from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10,)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_spam_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SpamNumber(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20,)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
