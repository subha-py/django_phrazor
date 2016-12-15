from django.shortcuts import (
    render,
    HttpResponse,
    get_object_or_404,
    redirect,
)
from django.urls import reverse



from files.forms import FileForm
from files.models import File,Field
from files.utils import (
    create_collection,
    get_summary_of_collection,
    get_collection,
    get_fields_and_data_from_collection,
    update_collection,
)


from reports.forms import ReportForm
from reports.models import Narrative,Segment

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
    collection_fields,document_list=get_fields_and_data_from_collection(collection_obj)
    context={
        'document_list':document_list,
        'collection_fields':collection_fields,
    }
    return render(request,'files/view.html',context)

def list_file(request):
    '''
    :param request:
    :return:a response
    '''

    report_form=ReportForm(request.POST or None)
    file_form = FileForm(request.POST or None, request.FILES or None)

    if file_form.is_valid():
        collection_name = create_collection(request, file_form)
        instance = file_form.save(commit=False)
        instance.collection = collection_name
        instance.save()
        collection_obj=get_collection(request,collection_name)
        field_list,_=get_fields_and_data_from_collection(collection_obj)
        field_instance_list=[]
        for turn in field_list:
            field_instance_list.append(Field.objects.create(
                name=turn[0],
                type=turn[1],
                file=instance)
            )
        print(Field.objects.all())
        return redirect(reverse('files:list'))

    elif report_form.is_valid():
        instance=report_form.save()
        narrative_instance=Narrative.objects.create(report=instance)
        narrative_instance.segments.create(index=0)
        print(instance.name,instance.file)
        return redirect(reverse('reports:editor',kwargs={'id':instance.id}))

    else:
        file_qs=File.objects.all()
        collection_list=[]
        for turn in file_qs:
            collection_list.append(get_summary_of_collection(request,turn))
        context={
            'collection_list':collection_list,
            'file_form':file_form,
            'report_form':report_form,
        }
        return render(request,'files/list.html',context)

def update_file(request,id):
    '''
    :param request:
    :return:
    '''
    instance = get_object_or_404(File, id=id)
    form = FileForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        collection_name = update_collection(request, form,pre_instance=instance)
        instance = form.save(commit=False)
        instance.collection = collection_name
        instance.save()
        return redirect(reverse('files:list'))
    else:
        return render(request, 'files/update.html', {'form': form})


################# JSON returning functions #############################
