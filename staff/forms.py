from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms

from .models import Worker


class WorkerRegisterForm(UserCreationForm):
    group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(WorkerRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'group']
