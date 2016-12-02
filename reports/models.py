from django.db import models
from files.models import File,Field


# Create your models here.
class Report(models.Model):
    name=models.CharField(max_length=255)
    file=models.ForeignKey(File,on_delete=models.CASCADE)
    text=models.TextField(blank=True)

    def __str__(self):
        return self.name

####################### Support Models ########################

class String_variables(models.Model):
    FORMAT_CHOICES=(
        ('','None'),
        ('CA','Capitalize'),
        ('UC','UPPERCASE'),
        ('LC','lowercase'),
        ('TC','Title Case'),


    )

    index=models.IntegerField()
    format=models.CharField(max_length=2,choices=FORMAT_CHOICES)
    field=models.ForeignKey(Field,on_delete=models.CASCADE)
    report=models.ForeignKey(Report,on_delete=models.CASCADE)

class Numeric_variables(models.Model):
    FORMAT_CHOICES = (
        ('AB', 'Absolute Value'),
        ('OR', 'Ordinal'),
        ('AP', 'AP format'),
        ('PE', 'Percentage'),
        ('CO','Commas'),
    )

    round=models.IntegerField()
    format=models.CharField(choices=FORMAT_CHOICES,max_length=2)
    index=models.IntegerField()
    field=models.ForeignKey(Field,on_delete=models.CASCADE)
    report=models.ForeignKey(Report,on_delete=models.CASCADE)


