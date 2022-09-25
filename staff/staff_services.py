from django.contrib.auth import get_user_model

from .models import Worker


def get_other_workers(current_worker_id):
    return get_user_model().objects.exclude(pk=current_worker_id).prefetch_related('groups')


def register_worker(form):
    worker = form.save()
    add_worker_to_group(worker, form.cleaned_data)


def add_worker_to_group(worker, cleaned_data):
    groups = cleaned_data['group']
    for group in groups:
        group.user_set.add(worker)
