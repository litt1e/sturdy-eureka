from django.db import models
from datetime import datetime

# Create your models here.


# TODO: добавить пользователя который создал тред/комент
class Answer(models.Model):
    user = models.CharField(max_length=20, default='AnonymousUser')
    text = models.TextField()
    date = models.DateTimeField(
        default=datetime.now()
    )
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Thread(models.Model):
    user = models.CharField(max_length=20, default='AnonymousUser')
    title = models.CharField(max_length=80)
    text = models.TextField()
    date = models.DateTimeField(
        default=datetime.now()
    )
    part = models.ForeignKey("Part", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Part(models.Model):
    title = models.CharField(max_length=40)
    short_title = models.CharField(max_length=4)
    section = models.ForeignKey("Section", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
