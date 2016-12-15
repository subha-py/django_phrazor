from django.shortcuts import render,HttpResponse,get_object_or_404
from reports.models import Report


from reports.utils import get_document_set




####create reports are handled at (files:list)

def editor(request,id):
    '''
    :param request:
    :return:
    '''

    report_obj=get_object_or_404(Report,id=id)
    document_set=get_document_set(report_obj=report_obj,number_of_documents=3)
    field_qs=report_obj.file.field_set.all()
    context={

        'report_obj':report_obj,
        'field_qs':field_qs,
        'document_set':document_set,
    }
    return render(request,'reports/editor.html',context)


def list_report(request):
    '''
    :param request:
    :return:
    '''
    report_qs=Report.objects.all()
    context={
        'report_qs':report_qs,
    }
    return render(request,'reports/list.html',context)





