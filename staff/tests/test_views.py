from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.test import Client


class GeneralWorkerTestCase(TestCase):
    def setUp(self):
        self.admin1 = get_user_model().objects.create_user(
            username='test_admin1',
            password='test_pw'
        )
        self.group1 = Group.objects.create(
            name='administrator'
        )
        self.group1.user_set.add(self.admin1)

        self.client = Client()
        self.client.login(username='test_admin1', password='test_pw')


class WorkersViewTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(WorkersViewTestCase, self).setUp()
        self.can_view_worker = Permission.objects.get(codename='view_worker')
        self.group1.permissions.add(self.can_view_worker)

    def test_view(self):
        response = self.client.get(reverse("staff:workers"), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='staff/workers.html')
        self.assertListEqual(
            response.context_data.get('table_head'),
            ['ID пользователя', 'Имя пользователя', 'Группа']
            )


class WorkerPageUpdateTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(WorkerPageUpdateTestCase, self).setUp()
        self.can_change_worker = Permission.objects.get(codename='change_worker')
        self.group1.permissions.add(self.can_change_worker)

    def test_view(self):
        response = self.client.get(f"/staff/{self.admin1.pk}", follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='staff/worker_page.html')


class WorkerPageDeleteTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(WorkerPageDeleteTestCase, self).setUp()
        self.can_delete_worker = Permission.objects.get(codename='delete_worker')
        self.group1.permissions.add(self.can_delete_worker)

    def test_view(self):
        response = self.client.get(f"/staff/{self.admin1.pk}/delete", follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='staff/worker_page_delete.html')


class RegisterWorkerTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(RegisterWorkerTestCase, self).setUp()
        self.can_register_worker = Permission.objects.get(codename='add_worker')
        self.group1.permissions.add(self.can_register_worker)

    def test_view(self):
        response = self.client.get(f"/staff/register/", follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='staff/register_worker.html')


class LoginWorkerTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(LoginWorkerTestCase, self).setUp()
        self.client2 = Client()

    def test_view(self):
        response2 = self.client.get(f"/staff/login/", follow=True)
        self.assertRedirects(response2, '/')

        response = self.client2.get(f"/staff/login/", follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='staff/login_worker.html')
