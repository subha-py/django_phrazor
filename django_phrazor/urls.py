from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^files/',include('files.urls',namespace='files')),
    url(r'^reports/',include('reports.urls',namespace='reports')),
    url(r'^',TemplateView.as_view(template_name='index.html'),name='home')
]
