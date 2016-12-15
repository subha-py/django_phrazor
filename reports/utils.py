from reports.models import Report
from files.models import File
from files.utils import get_mongodb_client


def get_collection_obj_from_file_obj(file_obj):
    '''
    :param file_obj:
    :return:
    '''
    client=get_mongodb_client()
    #TODO get database according to user
    db=client.test_database
    return db[file_obj.collection]


def get_document_set(report_obj=None,file_obj=None,number_of_documents=None):
    '''
    :param report_obj:Instance of Report class
    :param file_obj:Instance of File class
    :param number_of_documents: Number of documents required
    :return: a set of mongo_db documents
    '''
    if file_obj!=None and isinstance(file_obj,File):
        collection_obj=get_collection_obj_from_file_obj(file_obj)
        document_set=collection_obj.find({},{'_id':False},limit=number_of_documents)
        return list(document_set)
    elif report_obj!=None and isinstance(report_obj,Report):
        file_obj=report_obj.file
        return get_document_set(file_obj=file_obj,number_of_documents=number_of_documents)
    else:
        raise ValueError('Parameters are not correctly passed')
