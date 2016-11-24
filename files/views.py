from django.shortcuts import (
    render,
    HttpResponse,
    get_object_or_404,
    redirect,
)
from django.urls import reverse
from django.http import JsonResponse

from bson.json_util import dumps


from files.forms import FileForm
from files.models import File
from files.utils import (
    create_collection,
    get_summary_of_collection,
    get_collection,
    get_fields_from_collection,
)

# Create your views here.
def create_file(request):
    '''
    :param request:
    :return:
    '''
    form=FileForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        collection_name=create_collection(request,form)
        instance=form.save(commit=False)
        instance.collection=collection_name
        instance.save()
        return redirect(reverse('files:list'))
    else:
        return render(request,'files/create.html',{'form':form})


def view_file(request,name):
    '''
    :param request:
    :param name:
    :return:
    '''
    #TODO : user and name will be unique, will query by them

    instance=get_object_or_404(File,name=name)
    collection_obj=get_collection(request,instance.collection)
    collection_fields=get_fields_from_collection(collection_obj)
    context={
        'instance':instance,
        'collection_fields':collection_fields,
    }
    return render(request,'files/view.html',context)

def list_file(request):
    '''
    :param request:
    :return:a response
    '''
    file_qs=File.objects.all()
    collection_list=[]
    for turn in file_qs:
        collection_list.append(get_summary_of_collection(request,turn))
    context={
        'collection_list':collection_list
    }
    return render(request,'files/list.html',context)



################# JSON returning functions #############################
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def view_table(request,collection_name):
    '''
    This function returns json response to fill table in files view
    :param request:
    :return:
    '''
    collection_obj=get_collection(request,collection_name)
    document_list=JSONEncoder().encode(list(collection_obj.find()))
    return HttpResponse(document_list,content_type='application/json')