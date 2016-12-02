import os
import csv
import random
from itertools import islice
import ast

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
    field_names=getFieldnames(filepath)
    document_list=writeCursor(filepath,field_names)
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

def update_collection(request,form,pre_instance):
    '''
    :param request:
    :param form:
    :return:
    '''
    name=form.cleaned_data.get('name')
    client=get_mongodb_client()
    #todo : change database according to user
    db=client.test_database
    db.drop_collection(pre_instance.collection)
    return create_collection(request,form)



def get_fields_and_data_from_collection(collection_obj):
    #TODO: get samples of data and evaluate
    document_set=collection_obj.find({},{'_id':False},limit=50)
    demo_doc=document_set[0]
    demo_fields=list(demo_doc.keys())
    demo_values=list(demo_doc.values())
    field_list=[]
    for index,value in enumerate(demo_values):
        field_type=type(value).__name__
        if field_type=='float':
            field_type='int'
        field_list.append((demo_fields[index],field_type))
    return field_list,document_set


def get_summary_of_collection(request,file_obj):
    '''
    :param request: to get identify db as per user
    :param collection: collection obj
    :return: a summary to show in 'files:list'
    '''
    collection=get_collection(request,file_obj.collection)
    name=file_obj.collection
    field_list,x=get_fields_and_data_from_collection(collection)
    count_of_collection=collection.count()
    timestamp=file_obj.timestamp
    return [name,field_list,count_of_collection,timestamp,file_obj]


def getFieldnames(csvFile):
    """
    Read the first row and store values in a tuple
    """
    with open(csvFile) as csvfile:
        firstRow = csvfile.readlines(1)
        fieldnames = tuple(firstRow[0].strip('\n').split(","))
    return fieldnames

def writeCursor(csvFile, fieldnames):
    """
    Convert csv rows into an array of dictionaries
    All data types are automatically checked and converted
    """
    cursor = []  # Placeholder for the dictionaries/documents
    with open(csvFile) as csvFile:
        for row in islice(csvFile, 1, None):
            values = list(row.strip('\n').split(","))
            for i, value in enumerate(values):
                try:
                    nValue = ast.literal_eval(value)
                except:
                    nValue=value
                values[i] = nValue
            cursor.append(dict(zip(fieldnames, values)))
    return cursor