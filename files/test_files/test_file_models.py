import os

from django.test import TestCase
from django.contrib.auth.models import  User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError


from files.models import File

def get_test_file():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path=os.path.abspath(os.path.join(BASE_DIR, 'test_files/test.csv'))
    file = SimpleUploadedFile(name='test.csv', content=open(file_path, 'rb').read(),)
    return file



def get_user_obj_by_name(name='elspeth'):
    user_obj= User.objects.create_user(
        username=slugify(name),
        email='{name}@example.com'.format(name=name),
        password='{name}123'.format(name=name),
    )
    return user_obj



class FileModelTest(TestCase):

    def test_file_create(self):
        user_obj=get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj=File.objects.create(
            name='test_bank_revenue.csv',
            desc = 'Data of test banks revenue',
            file = get_test_file(),
            user = user_obj,
        )
        self.assertEqual(file_obj.name,'test_bank_revenue.csv')
        self.assertEqual(file_obj.desc,'Data of test banks revenue')

    def test_default_parameters(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        self.assertIsNotNone(file_obj.timestamp)

    def test_artist_cannot_have_duplicate_albums(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )

        with self.assertRaises(ValidationError):
            file_obj = File(
                name='test_bank_revenue.csv',
                desc='Data of test banks revenue',
                file=get_test_file(),
                user=user_obj,
            )
            file_obj.full_clean()

    def test_different_users_can_have_same_file_name(self):
        user_obj1 = get_user_obj_by_name()
        user_obj2 = get_user_obj_by_name(name='Zlatan Ibrahimovic')
        same_name='test_bank_revenue.csv'
        file_obj1 = File.objects.create(
            name=same_name,
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj1,
        )

        file_obj2 = File.objects.create(
            name=same_name,
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj2,
        )

        self.assertEqual(file_obj1.name,file_obj2.name)

    def test_one_user_can_have_many_files(self):
        user_obj = get_user_obj_by_name()
        file_obj1 = File.objects.create(
            name='demo file 1',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )

        file_obj2 = File.objects.create(
            name='demo file 2',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )

        self.assertEqual(File.objects.filter(user__username=user_obj.username).count(),2)

    def test_ordering_of_albums(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj1 = File.objects.create(
            name='test_bank_revenue1.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )

        file_obj2 = File.objects.create(
            name='test_bank_revenue2.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        file_obj3 = File.objects.create(
            name='test_bank_revenue3.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        file_obj4 = File.objects.create(
            name='test_bank_revenue4.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )


        self.assertEqual(list(File.objects.all()),[file_obj4,file_obj3,file_obj2,file_obj1])

    def test_string_representation(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue1.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        self.assertEqual(str(file_obj),'test_bank_revenue1.csv')