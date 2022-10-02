from django import forms

from .models import *


class AppealCreateForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ('FirstName', 'SecondName', 'ThirdName', 'SocialStatus',
                  'PhoneNumber', 'EmailAddress', 'PhysicalAddress', 'AppealContent')


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('UserExecutor', 'TaskContent',)


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('AnswerContent',)


class ReportCreateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('ReportContent',)
