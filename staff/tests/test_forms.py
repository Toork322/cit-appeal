from django.test import TestCase
from django.contrib.auth.models import Group

from staff.forms import WorkerRegisterForm


class WorkerRegisterFormTestCase(TestCase):
    def setUp(self):
        self.group1 = Group.objects.create(
            name='administrator'
        )
        form_data = {'username': 'username',
                     'password1': 'NuT8+uPw6^sfGbKn',
                     'password2': 'NuT8+uPw6^sfGbKn',
                     'group': (self.group1, ),
                     }
        self.form = WorkerRegisterForm(data=form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())
