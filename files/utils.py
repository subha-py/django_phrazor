import os
import csv

from django.conf import settings

from pymongo import MongoClient



##################### Django utilities ########################

def handle_uploaded_file(request,name):
    TEMP_ROOT = os.path.abspath(os.path.join(settings.BASE_DIR, '../temp'))

    f=request.FILES.get('file')
    #TODO: add username here in the directory
    filename='{temp_root}/{name}.csv'.format(
            temp_root=TEMP_ROOT,
            username=request.user.username,
            name=name)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    #TODO: add username here in the directory
    with open('{temp_root}/{name}.csv'.format(
            temp_root=TEMP_ROOT,
            username=request.user.username,
            name=name), 'wb') as destination:

        for chunk in f.chunks():
            destination.write(chunk)

    return filename


def csv_to_json(request,form):
    '''
    convert uploaded csv file to json
    :param request:
    :param form:
    :return:
    '''
    name=form.cleaned_data.get('name')
    filepath = handle_uploaded_file(request, name)
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        document_list = list(reader)
    os.remove(filepath)
    return document_list

######################################################################


######################## pymongo utility ###########################


def get_mongodb_client(url=settings.DATABASES['mongodb']['URL'],
                        port=settings.DATABASES['mongodb']['PORT']):
    '''
    :param ip/url: of the mongodb server.
    :param port: port to access
    :return: MongoClient object
    '''
    return MongoClient(url,port)

def get_collection(request,collection_name):
    '''
    This function returns collection object for user using name
    :param request: request will be used to get user object by request.user
    :param name: name of collection
    :return: mongodb collection object
    '''
    client=get_mongodb_client()
    #TODO : change database according to user
    db=client.test_database
    return db[collection_name]

def create_collection(request,form):
    '''
    :param request: comes from files:create or files:update
    :param form: FileForm object
    :return: collection object of mongodb
    '''
    name = form.cleaned_data.get('name')
    collection=get_collection(request,name)
    document_list=csv_to_json(request,form)
    collection.insert_many(document_list)
    return name


def get_fields_from_collection(collection_obj):
    demo_data = collection_obj.find_one()
    field_list = list(demo_data.keys())
    return field_list

def get_summary_of_collection(request,file_obj):
    '''
    :param request: to get identify db as per user
    :param collection: collection obj
    :return: a summary to show in 'files:list'
    '''
    collection=get_collection(request,file_obj.collection)
    name=file_obj.collection
    field_list=get_fields_from_collection(collection)
    field_list.remove('_id')
    field_list_string=', '.join(field_list)[:100]+'...'
    count_of_collection=collection.count()
    timestamp=file_obj.timestamp
    return [name,field_list_string,count_of_collection,timestamp,file_obj]