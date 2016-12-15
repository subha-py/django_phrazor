from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from files.models import File,Field


# Create your models here.
class Report(models.Model):
    name=models.CharField(max_length=255)
    file=models.ForeignKey(File,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

####################### Support Models ########################


class Segment(models.Model):
    '''
    Desc:
    '''
    index=models.PositiveIntegerField()
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')



class Narrative(models.Model):
    report=models.OneToOneField(Report)
    timestamp=models.DateTimeField(auto_now_add=True)
    segments=GenericRelation(Segment)


class Text(models.Model):
    '''
    desc:
    '''
    value=models.TextField()
    segments=models.ForeignKey(Segment,on_delete=models.CASCADE)

class Branch(models.Model):
    segments=models.ForeignKey(Segment,on_delete=models.CASCADE)

class Condition(models.Model):
    branches=models.ForeignKey(Branch)
    code=models.TextField()
    index=models.PositiveIntegerField()
    segments=GenericRelation(Segment,on_delete=models.CASCADE)

class Datavar(models.Model):
    name=models.ForeignKey(Field)
    absolute_value=models.BooleanField(default=False)
    apFormat=models.BooleanField(default=False)
    commas=models.BooleanField(default=True)
    decimal_seperator=models.CharField(max_length=1)
    language=models.CharField(max_length=2,default='EN')
    num_decimals=models.PositiveIntegerField()
    ordinal=models.BooleanField(default=False)
    significant_figures=models.PositiveIntegerField(default=0)
    large_number=models.BooleanField(default=False)
    num_decimal_millions=models.PositiveIntegerField(default=1)
    num_decimal_billions = models.PositiveIntegerField(default=2)
    num_decimals_huge = models.PositiveIntegerField(default=3)
    to_words=models.BooleanField(default=False)
    string_format=models.CharField(max_length=255)
    list_conjuntion=models.CharField(max_length=255,default='and')
    list_oxford_comma=models.BooleanField(default=True)


class Synonym(models.Model):
    segments=models.ForeignKey(Segment,on_delete=models.CASCADE)

class SynonymVariation(models.Model):
    synonym=models.ForeignKey(Synonym,on_delete=models.CASCADE)
    index=models.PositiveIntegerField()
    segments=GenericRelation(Segment,on_delete=models.CASCADE)