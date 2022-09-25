from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group


from appeal.forms import AppealCreateForm, TaskCreateForm, AnswerCreateForm, ReportCreateForm


class AppealCreateFormTestCase(TestCase):
    def setUp(self):
        form_data = {'FirstName': 'Ivan',
                     'SecondName': 'Ivanov',
                     'ThirdName': 'Ivanovich',
                     'SocialStatus': 'Пенсионер',
                     'PhoneNumber': '79999999999',
                     'EmailAddress': 'asd@asd.asd',
                     'PhysicalAddress': 'Izhevsk',
                     'AppealContent': 'Необходимо тщательно мытье лестницы на '
                                      'всех этажах с применением чистящих средств',
                     }
        self.form = AppealCreateForm(data=form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())


class TaskCreateFormTestCase(TestCase):
    def setUp(self):
        self.group1 = Group.objects.create(
            name='administrator'
        )
        self.group2 = Group.objects.create(
            name='executor'
        )
        self.exec1 = get_user_model().objects.create_user(
            username='test_executor1',
            password='test_pw'
        )
        self.group2.user_set.add(self.exec1)
        form_data = {'UserExecutor': self.exec1,
                     'TaskContent': 'Необходимо тщательно мытье лестницы на '
                                    'всех этажах с применением чистящих средств'
                     }
        self.form = TaskCreateForm(data=form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())


class AnswerCreateFormTestCase(TestCase):
    def setUp(self):
        form_data = {
            'AnswerContent': 'Необходимо тщательно мытье лестницы на '
                             'всех этажах с применением чистящих средств',
        }
        self.form = AnswerCreateForm(data=form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())


class ReportCreateFormTestCase(TestCase):
    def setUp(self):
        form_data = {
            'ReportContent': 'Необходимо тщательно мытье лестницы на '
                             'всех этажах с применением чистящих средств',
        }
        self.form = ReportCreateForm(data=form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())
