from django.conf.urls import url

from reports.views import (
    create_report,
)


urlpatterns = [
    url(r'^create/',create_report,name='create'),
]
