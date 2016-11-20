from django.test import TestCase,Client
from django.core.urlresolvers import reverse

from files.test_files.test_file_models import get_test_file,get_user_obj_by_name
from files.models import File




class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')


class CreateFileTest(TestCase):

    def test_saving_a_POST_request(self):
        user_obj=get_user_obj_by_name()
        c = Client()
        c.force_login(user_obj, backend=None)
        response=c.post(
            reverse('files:create'),
            data={'name': 'DemoFile','desc':'This is a demo description','file':get_test_file()},
        )
        self.assertEqual(File.objects.all().count(), 1)
        new_file = File.objects.first()
        self.assertEqual(new_file.name, 'DemoFile')
        self.assertEqual(new_file.user.id,user_obj.id)

    def test_redirects_after_POST(self):
        user_obj = get_user_obj_by_name()
        c = Client()
        c.force_login(user_obj, backend=None)
        response = c.post(
            reverse('files:create'),
            data={'name': 'DemoFile', 'desc': 'This is a demo description', 'file': get_test_file()},
        )
        self.assertEqual(File.objects.all().count(), 1)
        new_file = File.objects.first()
        self.assertRedirects(response, reverse('files:view',kwargs={'name':new_file.name}))


    def test_for_create_view_uses_correct_html(self):
        response = self.client.get(reverse('files:create'))
        self.assertTemplateUsed(response, 'files/create.html')




class ViewFileTest(TestCase):

    def test_uses_correct_template(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        c = Client()
        c.force_login(user_obj)
        response = c.get(reverse('files:view',kwargs={'name':file_obj.name}))
        self.assertTemplateUsed(response, 'files/view.html')


    def test_uses_correct_instance(self):
        user_obj = get_user_obj_by_name('Zlatan Ibrahimovic')
        file_obj = File.objects.create(
            name='test_bank_revenue.csv',
            desc='Data of test banks revenue',
            file=get_test_file(),
            user=user_obj,
        )
        c = Client()
        c.force_login(user_obj)
        response = c.get(reverse('files:view', kwargs={'name': file_obj.name}))
        self.assertEqual(response.context['instance'], file_obj)
