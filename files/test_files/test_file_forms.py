from django.contrib.auth import get_user_model
from django.test import TestCase


from files.test_files.test_file_models import get_user_obj_by_name,get_test_file
from files.models import File
from files.forms import FileForm

User=get_user_model()


class FileFormTest(TestCase):

    def test_form_can_be_validated(self):
        form = FileForm(data={
            'name':'Demo Name',
            'desc':'This is a demo description',
        },
            files={
                'file':get_test_file()
            })


        self.assertTrue(form.is_valid())

    def test_form_can_save_data_in_db(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        form = FileForm(data={
            'name':'Demo Name',
            'desc':'This is a demo description',
        },
            files={
                'file':get_test_file()
            })
        if form.is_valid():
            instance=form.save(user_obj)

        file_obj=File.objects.first()
        self.assertEqual(file_obj.name,instance.name)
        self.assertEqual(file_obj.desc,instance.desc)
        self.assertEqual(file_obj.user.username,instance.user.username)
        self.assertEqual(file_obj.file,instance.file)


    def test_form_can_update_file_info(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        form = FileForm(instance=file_obj,
                        data={
                            'name': 'Demo Name',
                            'desc': 'This is a demo description',
                        },
                        files={
                            'file': get_test_file()
                        })
        if form.is_valid():
            instance = form.save(user_obj)

        self.assertEqual(File.objects.count(),1)
        file_obj=File.objects.first()
        self.assertEqual(file_obj.name,instance.name)
        self.assertEqual(file_obj.desc,instance.desc)
        self.assertEqual(file_obj.file,instance.file)
