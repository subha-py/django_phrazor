import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_phrazor.settings")
from django.conf import settings
from files.utils import get_mongodb_client



client=get_mongodb_client()
db=client.test_database
collection_list=db.collection_names()
for turn in collection_list:
    print(turn)
    db.drop_collection(turn)

if len(db.collection_names())>1:
    print('mongo collections are still not clear')
else:
    print('Good to go!')