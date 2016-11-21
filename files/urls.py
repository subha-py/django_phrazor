from django.conf.urls import url

from files.views import (
    create_file,
    view_file,
    list_file,
)


urlpatterns = [
    url(r'^create/',create_file,name='create'),
    # url(r'^view/(?P<name>[\w-]+)/$', view_file, name='view'),
    url(r'^list/',list_file,name='list'),
    url(r'^(?P<name>.*)/view/$', view_file, name='view'),
]
