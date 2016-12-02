from django.shortcuts import render,HttpResponse


from reports.forms import DasboardForm
# Create your views here.


def create_report(request):
    '''
    :param request:
    :return:
    '''
    form=DasboardForm(request.POST or None)

    if form.is_valid():
        form.save()
    else:
        context={
            'form':form,
        }
        return render(request,'dashboards/index.html',context)