from django.contrib.auth import get_user_model
from django.test import TestCase
from appeal.models import Appeal, Task, Category, Status
from django.contrib.auth.models import Group
from workspace.workspace_services import get_table_data_for_user


class GettingDataTestCase(TestCase):
    def setUp(self):
        self.category_ad = Category.objects.create(
            CategoryValue='Реклама'
        )
        self.status_waiting = Status.objects.create(
            StatusValue='В ожидании'
        )
        self.appeal = Appeal.objects.create(
            FirstName='Ivan',
            SecondName='Ivanov',
            ThirdName='Ivanovich',
            SocialStatus='Пенсия',
            PhoneNumber='123',
            EmailAddress='asd@asd.asd',
            PhysicalAddress='asdasd',
            AppealContent='asdasdasd',
            CategoryValue=self.category_ad,
            AppealStatus=self.status_waiting
        )

        self.admin1 = get_user_model().objects.create(
            username='test_admin1',
            password='test_pw'
        )
        self.group1 = Group.objects.create(
            name='administrator'
        )
        self.group1.user_set.add(self.admin1)

        self.exec1 = get_user_model().objects.create(
            username='test_executor1',
            password='test_pw'
        )
        self.group2 = Group.objects.create(
            name='executor'
        )
        self.group2.user_set.add(self.exec1)

        self.task = Task.objects.create(
            UserExecutor=self.exec1,
            CurrentAppeal=self.appeal,
            TaskStatus=self.status_waiting,
            TaskContent='asdasd',
        )

    def test_admin_correct_data(self):
        data, table_head, header = get_table_data_for_user(self.admin1)
        self.assertQuerysetEqual(
            Appeal.objects.all().select_related('CategoryValue', 'AppealStatus'),
            data
        )
        self.assertTupleEqual(
            ('ID', 'Заголовок', 'Дата отправки', 'Статус', 'Категория'),
            table_head
        )
        self.assertEqual(
            'Входящие обращения',
            header
        )

    def test_executor_correct_data(self):
        data, table_head, header = get_table_data_for_user(self.exec1)
        self.assertQuerysetEqual(
            Task.objects.filter(UserExecutor=self.exec1),
            data
        )
        self.assertTupleEqual(
            ('ID', 'Содержание', 'Дата постановки', 'Статус'),
            table_head
        )
        self.assertEqual(
            'Задачи',
            header
        )
