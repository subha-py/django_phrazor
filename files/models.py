from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import JSONField

from picklefield.fields import PickledObjectField

def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/username/filename
    return 'data/{user}/{file_name}.png'.format(user=instance.user.username,file_name=instance.name)



class File(models.Model):
    '''
    A file object class
    '''
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='file')
    name=models.CharField(max_length=255)
    desc=models.CharField(max_length=255)
    data=JSONField()
    data2=PickledObjectField()
    #structure oj json field:{'content':
    #                           [
    #                               {'sex': 'm', 'name': 'subha', 'age': '22', 'position': 'full stack developer'},
    #                               {'sex': 'm', 'name': 'vivek', 'age': '25', 'position': 'data scientist'}
    #                           ], #these dictionaries are rows in excel or csv files
    #
    #                         'meta': Not decided yet
    #                       }
    #
    #
    timestamp=models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['name', 'user']
        ordering = ['-timestamp']



    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("files:view", kwargs={"name": self.name})


    # def get_stats(self):
    #     '''
    #     :return: [{'field_name':field_name,'max':max_value,'min':min_value,'avg': avg_value},]
    #     '''
    #     data_qs=self.data.get('content')
    #     test_data=data_qs[0]
    #     num_fields=[]
    #     for turn in test_data:
    #         if type(test_data.get(turn)) in [type(1),type(1.00)]:
    #             num_fields.append(turn)
    #
    #
    #     data_list=[]
    #     for turn in num_fields:

