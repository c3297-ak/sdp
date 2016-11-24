from django.db import models


# Create your models here.

class Staff(models.Model):
    username = models.CharField(max_length=8)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Participant(Staff):
    def __str__(self):
        return "Participant: " + self.username


class Instructor(Staff):
    def __str__(self):
        return 'Instructor: ' + self.username
