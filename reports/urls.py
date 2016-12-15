from django.conf.urls import url

from reports.views import (
    editor,
    list_report,

)


urlpatterns = [
    url(r'^(?P<id>[0-9]+)/editor/',editor,name='editor'),
    # url(r'^(?P<id>[0-9]+)/view/',view_report,name='view'),
    url(r'^list/',list_report,name='list'),

]
