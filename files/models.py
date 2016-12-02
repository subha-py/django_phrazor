from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse


class File(models.Model):
    '''
    A file object class
    '''
    # user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='file')
    name=models.CharField(max_length=255,unique=True)
    desc=models.CharField(max_length=255)
    collection=models.CharField(max_length=255)
    timestamp=models.DateTimeField(auto_now_add=True)


    class Meta:
        #unique_together = ['name', 'user']
        ordering = ['-timestamp']



    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("files:view", kwargs={"name": self.name})


class Field(models.Model):
    '''
    A field object
    '''
    DATA_TYPE_CHOICES=(
        ('Integer','int'),
        ('String','str')
    )

    name=models.CharField(max_length=255)
    data_type=models.CharField(max_length=10,choices=DATA_TYPE_CHOICES,default='str')
    file=models.ForeignKey(File,on_delete=models.CASCADE)

    def __str__(self):
        return '{name}({field})'.format(name=self.name,field=self.data_type)