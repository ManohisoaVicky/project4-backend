from django.db import models
from django.conf import settings
# Create your models here.

class Event(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participants", blank=True)

    def __str__(self):
        return self.name