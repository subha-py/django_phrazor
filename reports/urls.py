from django.conf.urls import url

from reports.views import (
    create_reports,
)


urlpatterns = [
    url(r'^create/',create_reports,name='create'),

]
