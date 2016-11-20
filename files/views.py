from django.shortcuts import (
    render,
    HttpResponse,
    get_object_or_404,
    redirect,
)

from files.forms import FileForm
from files.models import File


# Create your views here.
def create_file(request):
    '''
    :param request:
    :return:
    '''
    form=FileForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance=form.save(request.user)
        return redirect(instance.get_absolute_url())
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