from django.shortcuts import render,HttpResponse


from reports.forms import ReportForm
# Create your views here.
def create_reports(request):
    '''
    :param request:
    :return:
    '''
    form=ReportForm(request.POST)
    if form.is_valid():
        instance=form.save()
        print(instance.name,instance.collection,'I am here')
        return HttpResponse('Check console')
    else:
        return render(request,)