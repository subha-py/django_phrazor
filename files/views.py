import csv
import pprint
import os
import pandas as pd

from django.shortcuts import (
    render,
    HttpResponse,
    get_object_or_404,
    redirect,
)


from files.forms import FileForm
from files.models import File
from files.utils import handle_uploaded_file


# Create your views here.
def create_file(request):
    '''
    :param request:
    :return:
    '''
    form=FileForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        name=form.cleaned_data.get('name')
        filepath=handle_uploaded_file(request,name)
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            reader=list(reader)
        df=pd.read_csv(filepath)
        print(df)

        os.remove(filepath)
        instance=form.save(request.user,commit=False)
        instance.data={
            'content':reader
        }
        instance.data2=df
        instance.save()
        return HttpResponse(instance.data2)
    else:
        return render(request,'files/create.html',{'form':form})


def view_file(request,name):
    '''
    :param request:
    :param name:
    :return:
    '''
    instance=get_object_or_404(File,name=name,user=request.user)
    return render(request,'files/view.html',{'instance':instance})

def list_file(request):
    '''
    :param request:
    :return:a response
    '''
    file_qs=File.objects.filter(user__username=request.user.username)
    return render(request,'files/list.html',{'file_qs':file_qs})