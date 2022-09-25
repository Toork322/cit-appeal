from django import forms
from crispy_forms.helper import FormHelper

from .models import *


class AppealCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppealCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Appeal
        fields = ('FirstName', 'SecondName', 'ThirdName', 'SocialStatus',
                  'PhoneNumber', 'EmailAddress', 'PhysicalAddress', 'AppealContent')


class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Task
        fields = ('UserExecutor', 'TaskContent',)


class AnswerCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Answer
        fields = ('AnswerContent',)


class ReportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Report
        fields = ('ReportContent',)
