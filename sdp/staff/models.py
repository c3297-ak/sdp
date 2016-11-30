from django.db import models


# Create your models here.

class Staff(models.Model):
    username = models.CharField(max_length=8)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Permission(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    class Meta:
        abstract=True


class Participant(Permission):
    def __str__(self):
        return 'Participant permission'


class Instructor(Permission):
    def __str__(self):
        return 'Instructor permission'


class Administrator(Permission):
    def __str__(self):
        return 'Administrator permission'


class HumanResource(Permission):
    def __str__(self):
        return 'HR permission'
