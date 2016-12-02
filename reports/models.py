from django.db import models
from files.models import File


# Create your models here.
class Report(models.Model):
    name=models.CharField(max_length=255)
    file=models.ForeignKey(File,on_delete=models.CASCADE)
    text=models.TextField()
