from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms


class WorkerRegisterForm(UserCreationForm):
    group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'group']
