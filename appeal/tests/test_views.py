from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.test import Client
from django.urls import reverse

from appeal.models import Status, Appeal, Category, Task, Answer, Report


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

        self.exec1 = get_user_model().objects.create_user(
            username='test_exec1',
            password='test_pw'
        )
        self.group2 = Group.objects.create(
            name='executor'
        )
        self.group2.user_set.add(self.exec1)

        self.client = Client()

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
        self.task = Task.objects.create(
            UserExecutor=self.exec1,
            CurrentAppeal=self.appeal,
            TaskContent='asdasd asdasd',
            TaskStatus=self.status_waiting
        )
        self.answer = Answer.objects.create(
            CurrentAppeal=self.appeal,
            AnswerContent='asdasd aasd'
        )
        self.report = Report.objects.create(
            CurrentTask=self.task,
            ReportContent='asdasd aasd'
        )


class CreateAppealTestCase(GeneralWorkerTestCase):
    def test_status_code(self):
        response = self.client.get(reverse("appeal:create_appeal"), follow=True)
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(reverse("appeal:create_appeal"), follow=True)
        self.assertTemplateUsed(response, template_name='appeal/create_appeal.html')


class AppealCardTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(AppealCardTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_view_appeal = Permission.objects.get(codename='view_appeal')
        self.group1.permissions.add(self.can_view_appeal)
        self.can_change_appeal = Permission.objects.get(codename='change_appeal')
        self.group1.permissions.add(self.can_change_appeal)

    def test_status_code(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}", follow=True)
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}", follow=True)
        self.assertTemplateUsed(response, template_name='appeal/appeal_card.html')


class AppealDeleteTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(AppealDeleteTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_delete_appeal = Permission.objects.get(codename='delete_appeal')
        self.group1.permissions.add(self.can_delete_appeal)

    def test_status_code(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/delete", follow=True)
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/delete", follow=True)
        self.assertTemplateUsed(response, template_name='appeal/appeal_confirm_action.html')


class CreateTaskTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(CreateTaskTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_add_task = Permission.objects.get(codename='add_task')
        self.group1.permissions.add(self.can_add_task)

    def test_status_code(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/create_task", follow=True)
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/create_task", follow=True)
        self.assertTemplateUsed(response, template_name='appeal/create_task.html')


class TaskCardTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(TaskCardTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_view_task = Permission.objects.get(codename='view_task')
        self.group1.permissions.add(self.can_view_task)

        self.can_change_task = Permission.objects.get(codename='change_task')
        self.group1.permissions.add(self.can_change_task)

    def test_status_code(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/task/{self.task.pk}", follow=True)
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(f"/appeal/{self.appeal.pk}/task/{self.task.pk}", follow=True)
        self.assertTemplateUsed(response, template_name='appeal/task_card.html')


class TaskDeleteTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(TaskDeleteTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_delete_task = Permission.objects.get(codename='delete_task')
        self.group1.permissions.add(self.can_delete_task)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/delete",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/delete",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/appeal_confirm_action.html')


class CreateAnswerTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(CreateAnswerTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_add_answer = Permission.objects.get(codename='add_answer')
        self.group1.permissions.add(self.can_add_answer)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/create_answer",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/create_answer",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/create_answer.html')


class AnswerCardTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(AnswerCardTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_view_answer = Permission.objects.get(codename='view_answer')
        self.group1.permissions.add(self.can_view_answer)

        self.can_change_answer = Permission.objects.get(codename='change_answer')
        self.group1.permissions.add(self.can_change_answer)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/answer/{self.answer.pk}",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/answer/{self.answer.pk}",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/answer_card.html')


class AnswerDeleteTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(AnswerDeleteTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_delete_answer = Permission.objects.get(codename='delete_answer')
        self.group1.permissions.add(self.can_delete_answer)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/answer/{self.answer.pk}/delete",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/answer/{self.answer.pk}/delete",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/appeal_confirm_action.html')


class CreateReportTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(CreateReportTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_add_report = Permission.objects.get(codename='add_report')
        self.group1.permissions.add(self.can_add_report)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/create_report",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/create_report",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/create_report.html')


class ReportCardTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(ReportCardTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_view_report = Permission.objects.get(codename='view_report')
        self.group1.permissions.add(self.can_view_report)

        self.can_change_report = Permission.objects.get(codename='change_report')
        self.group1.permissions.add(self.can_change_report)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/report/{self.report.pk}",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/report/{self.report.pk}",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/report_card.html')


class ReportDeleteTestCase(GeneralWorkerTestCase):
    def setUp(self):
        super(ReportDeleteTestCase, self).setUp()
        self.client.login(username='test_admin1', password='test_pw')

        self.can_delete_report = Permission.objects.get(codename='delete_report')
        self.group1.permissions.add(self.can_delete_report)

    def test_status_code(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/report/{self.report.pk}/delete",
            follow=True
        )
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(
            f"/appeal/{self.appeal.pk}/task/{self.task.pk}/report/{self.report.pk}/delete",
            follow=True
        )
        self.assertTemplateUsed(response, template_name='appeal/appeal_confirm_action.html')