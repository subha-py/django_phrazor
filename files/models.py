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
