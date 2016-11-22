from django.conf import settings
import os


TEMP_ROOT = os.path.abspath(os.path.join(settings.BASE_DIR, '../temp'))


def handle_uploaded_file(request,name):
    f=request.FILES.get('file')
    filename='{temp_root}/{username}/{name}'.format(
            temp_root=TEMP_ROOT,
            username=request.user.username,
            name=name)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open('{temp_root}/{username}/{name}'.format(
            temp_root=TEMP_ROOT,
            username=request.user.username,
            name=name), 'wb') as destination:

        for chunk in f.chunks():
            destination.write(chunk)

    return filename