from django.contrib.auth import get_user_model
from django.test import TestCase
from staff.forms import WorkerRegisterForm
from django.contrib.auth.models import Group

from staff.staff_services import get_other_workers, register_worker


class GettingWorkersTestCase(TestCase):
    def setUp(self):
        self.admin1 = get_user_model().objects.create_user(
            username='test_admin1',
            password='test_pw'
        )
        self.group1 = Group.objects.create(
            name='administrator'
        )
        self.group1.user_set.add(self.admin1)

        self.exec1 = get_user_model().objects.create_user(
            username='test_executor1',
            password='test_pw'
        )
        self.group2 = Group.objects.create(
            name='executor'
        )
        self.group2.user_set.add(self.exec1)

        form_data = {'username': 'username',
                     'password1': 'NuT8+uPw6^sfGbKn',
                     'password2': 'NuT8+uPw6^sfGbKn',
                     'group': (self.group1,),
                     }
        self.form = WorkerRegisterForm(data=form_data)

    def test_get_other_workers(self):
        self.assertQuerysetEqual(
            get_user_model().objects.exclude(pk=self.exec1.pk).prefetch_related('groups'),
            get_other_workers(self.exec1.pk)
        )

    def test_register_worker(self):
        register_worker(self.form)
        self.assertTrue(
            get_user_model().objects.filter(username='username').exists()
        )
