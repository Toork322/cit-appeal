from django.shortcuts import get_object_or_404

from .models import Report, Task
from .appeal_services import get_appeal_from_id


def get_tasks_for_appeal(appeal_id):
    return Task.objects.filter(CurrentAppeal__pk=appeal_id).\
        select_related('UserExecutor', 'CurrentAppeal')


def get_task_from_id(task_id):
    return get_object_or_404(Task, pk=task_id)


def get_reports_for_task(task_id):
    return Report.objects.filter(CurrentTask__pk=task_id).\
        select_related('CurrentTask', 'CurrentTask__CurrentAppeal')


def save_task(self, form):
    form.instance.CurrentAppeal = get_appeal_from_id(self.kwargs['appeal_id'])
    form.save()
