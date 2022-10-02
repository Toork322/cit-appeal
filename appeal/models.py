from django.db import models
from django.urls import reverse, reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField

from citappeal import settings


class Status(models.Model):
    """Общий статус."""
    StatusValue = models.CharField(
        verbose_name='Статус',
        max_length=20
    )

    def __str__(self):
        return self.StatusValue


class Category(models.Model):
    """Категория обращения."""
    CategoryValue = models.CharField(
        verbose_name='Категория',
        max_length=255
    )

    def __str__(self):
        return self.CategoryValue


class Appeal(models.Model):
    """Обращение гражданина."""
    FirstName = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    SecondName = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    ThirdName = models.CharField(
        verbose_name='Отчество',
        max_length=255
    )
    SocialStatus = models.CharField(
        verbose_name='Социальный статус',
        max_length=255
    )
    PhoneNumber = PhoneNumberField(
        region='RU',
        blank=True,
        verbose_name='Номер телефона'
    )
    EmailAddress = models.EmailField(
        verbose_name='Email',
        max_length=255
    )
    PhysicalAddress = models.CharField(
        verbose_name='Адрес',
        max_length=255
    )
    AppealContent = models.TextField(
        verbose_name='Текст обращения'
    )
    DateApplication = models.DateField(
        verbose_name='Дата отправки',
        auto_now_add=True
    )
    DateRegistration = models.DateField(
        verbose_name='Дата регистрации',
        blank=True,
        null=True
    )

    CategoryValue = models.ForeignKey(
        Category,
        verbose_name='Категория обращения',
        on_delete=models.CASCADE
    )
    AppealStatus = models.ForeignKey(
        Status,
        verbose_name='Статус обращения',
        on_delete=models.CASCADE,
        default=1
    )

    def get_absolute_url(self):
        return reverse(
            'appeal:appeal_card',
            kwargs={'appeal_id': self.pk}
        )

    def __str__(self):
        return self.AppealContent[:50] + "..."


class Task(models.Model):
    """Задача по обращению для исполнителя."""
    UserExecutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Исполнитель',
        on_delete=models.CASCADE,
        limit_choices_to={'groups': '2'}
    )
    CurrentAppeal = models.ForeignKey(
        Appeal,
        verbose_name='Текущее обращение',
        on_delete=models.CASCADE
    )

    TaskStatus = models.ForeignKey(
        Status,
        verbose_name='Статус обращения',
        on_delete=models.CASCADE,
        null=True,
        default=1
    )

    TaskContent = models.TextField(
        verbose_name='Содержание'
    )
    DateTasking = models.DateField(
        verbose_name='Дата постановки',
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse(
            'appeal:task_card',
            kwargs={
                'appeal_id': self.CurrentAppeal.pk,
                'task_id': self.pk
            }
        )

    def __str__(self):
        return self.TaskContent[:50] + "..."


class Answer(models.Model):
    """Ответ гражданину."""
    CurrentAppeal = models.ForeignKey(
        Appeal,
        verbose_name='Обращение',
        on_delete=models.CASCADE
    )
    AnswerContent = models.TextField(
        verbose_name='Текст ответа'
    )
    DateCreation = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse(
            'appeal:answer_card',
            kwargs={
                'appeal_id': self.CurrentAppeal.pk,
                'answer_id': self.pk
            }
        )

    def __str__(self):
        return self.AnswerContent[:50] + "..."


class Report(models.Model):
    """Отчёт исполнителя по задаче."""
    CurrentTask = models.ForeignKey(
        Task,
        verbose_name='Текущая задача',
        on_delete=models.CASCADE
    )
    ReportContent = models.TextField(
        verbose_name='Содержание отчёта'
    )
    DateCreation = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse(
            'appeal:report_card',
            kwargs={
                'appeal_id': self.CurrentTask.CurrentAppeal.pk,
                'task_id': self.CurrentTask.pk,
                'report_id': self.pk
            }
        )

    def __str__(self):
        return self.ReportContent[:50] + "..."
