from django.conf.urls import url

from files.views import (
    create_file,
    view_file,
    list_file,
    update_file,
)


urlpatterns = [
    url(r'^create/',create_file,name='create'),
    url(r'^list/',list_file,name='list'),
    url(r'^(?P<name>[-\w.]+)/view/$', view_file, name='view'),
    url(r'^(?P<id>[0-9]+)/update/$', update_file, name='update'),
]
