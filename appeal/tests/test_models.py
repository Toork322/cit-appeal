from django.contrib.auth import get_user_model
from django.test import TestCase
from appeal.models import Status, Category, Appeal, Task, Answer, Report
from django.urls import reverse
from django.contrib.auth.models import Group


class GeneralTestCase(TestCase):
    def setUp(self):
        self.status_waiting = Status.objects.create(
            StatusValue='В ожидании'
        )
        self.category_ad = Category.objects.create(
            CategoryValue='Реклама'
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

        self.task = Task.objects.create(
            UserExecutor=self.exec1,
            CurrentAppeal=self.appeal,
            TaskContent='asdasd asdasd',
            TaskStatus=self.status_waiting
        )


class StatusTestCase(GeneralTestCase):
    def test_str(self):
        self.assertEqual(self.status_waiting.__str__(), 'В ожидании')


class CategoryTestCase(GeneralTestCase):
    def test_str(self):
        self.assertEqual(self.category_ad.__str__(), 'Реклама')


class AppealTestCase(GeneralTestCase):
    def test_get_absolute_url(self):
        url = reverse(
            'appeal:appeal_card',
            kwargs={'appeal_id': self.appeal.pk}
        )
        self.assertEqual(url, self.appeal.get_absolute_url())

    def test_str(self):
        self.assertEqual(self.appeal.__str__(), self.appeal.AppealContent[:50] + "...")


class TaskTestCase(GeneralTestCase):
    def test_get_absolute_url(self):
        url = reverse(
            'appeal:task_card',
            kwargs={
                'appeal_id': self.task.CurrentAppeal.pk,
                'task_id': self.task.pk
            }
        )
        self.assertEqual(url, self.task.get_absolute_url())

    def test_str(self):
        self.assertEqual(self.task.__str__(), self.task.TaskContent[:50] + "...")


class AnswerTestCase(GeneralTestCase):
    def setUp(self):
        super(AnswerTestCase, self).setUp()
        self.answer = Answer.objects.create(
            CurrentAppeal=self.appeal,
            AnswerContent='asdasd aasd'
        )

    def test_get_absolute_url(self):
        url = reverse(
            'appeal:answer_card',
            kwargs={
                'appeal_id': self.answer.CurrentAppeal.pk,
                'answer_id': self.answer.pk
            }
        )
        self.assertEqual(url, self.answer.get_absolute_url())

    def test_str(self):
        self.assertEqual(self.answer.__str__(), self.answer.AnswerContent[:50] + "...")


class ReportTestCase(GeneralTestCase):
    def setUp(self):
        super(ReportTestCase, self).setUp()
        self.report = Report.objects.create(
            CurrentTask=self.task,
            ReportContent='asdasd aasd'
        )

    def test_get_absolute_url(self):
        url = reverse(
            'appeal:report_card',
            kwargs={
                'appeal_id': self.report.CurrentTask.CurrentAppeal.pk,
                'task_id': self.report.CurrentTask.pk,
                'report_id': self.report.pk
            }
        )
        self.assertEqual(url, self.report.get_absolute_url())

    def test_str(self):
        self.assertEqual(self.report.__str__(), self.report.ReportContent[:50] + "...")
