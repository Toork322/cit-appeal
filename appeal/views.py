from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AppealCreateForm, TaskCreateForm, AnswerCreateForm, ReportCreateForm
from .models import Appeal, Task, Answer, Report
from .appeal_services import get_appeal_from_id, set_category_for_appeal
from .task_services import get_tasks_for_appeal, get_task_from_id, get_reports_for_task, save_task
from .answers_services import get_answers_for_appeal


class CreateAppeal(CreateView):
    form_class = AppealCreateForm
    template_name = 'appeal/create_appeal.html'

    def form_valid(self, form):
        set_category_for_appeal(form)
        return HttpResponse('Обращение отправлено.')


class AppealCard(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Appeal
    template_name = 'appeal/appeal_card.html'
    fields = '__all__'
    pk_url_kwarg = 'appeal_id'
    context_object_name = 'appeal'
    permission_required = ['appeal.view_appeal', 'appeal.change_appeal']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = get_tasks_for_appeal(self.kwargs['appeal_id'])
        context['answers'] = get_answers_for_appeal(self.kwargs['appeal_id'])
        return context


class AppealDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Appeal
    template_name = 'appeal/appeal_confirm_action.html'
    success_url = reverse_lazy('workspace')
    pk_url_kwarg = 'appeal_id'
    permission_required = ['appeal.delete_appeal']


class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = 'appeal/create_task.html'
    permission_required = ['appeal.add_task']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appeal_id'] = self.kwargs['appeal_id']
        return context

    def form_valid(self, form):
        save_task(self, form)
        return redirect('appeal:appeal_card', appeal_id=self.kwargs['appeal_id'])


class TaskCard(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'appeal/task_card.html'
    fields = '__all__'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    permission_required = ['appeal.view_task', 'appeal.change_task']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = get_reports_for_task(self.kwargs['task_id'])
        context['appeal_id'] = self.kwargs['appeal_id']
        context['task_id'] = self.kwargs['task_id']
        return context


class TaskDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'appeal/appeal_confirm_action.html'
    pk_url_kwarg = 'task_id'
    permission_required = ['appeal.delete_task']

    def get_success_url(self):
        return reverse(
            'appeal:appeal_card',
            kwargs={
                'appeal_id': self.kwargs['appeal_id']
            }
        )


class CreateAnswer(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AnswerCreateForm
    template_name = 'appeal/create_answer.html'
    permission_required = ['appeal.add_answer']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appeal_id'] = self.kwargs['appeal_id']
        return context

    def form_valid(self, form):
        form.instance.CurrentAppeal = get_appeal_from_id(self.kwargs['appeal_id'])
        form.save()
        return redirect('appeal:appeal_card', appeal_id=self.kwargs['appeal_id'])


class AnswerCard(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Answer
    template_name = 'appeal/answer_card.html'
    fields = '__all__'
    pk_url_kwarg = 'answer_id'
    context_object_name = 'answer'
    permission_required = ['appeal.view_answer', 'appeal.change_answer']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appeal_id'] = self.kwargs['appeal_id']
        context['answer_id'] = self.kwargs['answer_id']
        return context


class AnswerDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Answer
    template_name = 'appeal/appeal_confirm_action.html'
    pk_url_kwarg = 'answer_id'
    permission_required = ['appeal.delete_answer']

    def get_success_url(self):
        return reverse(
            'appeal:appeal_card',
            kwargs={
                'appeal_id': self.kwargs['appeal_id']
            })


class CreateReport(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ReportCreateForm
    template_name = 'appeal/create_report.html'
    permission_required = ['appeal.add_report']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appeal_id'] = self.kwargs['appeal_id']
        context['task_id'] = self.kwargs['task_id']
        return context

    def form_valid(self, form):
        form.instance.CurrentTask = get_task_from_id(self.kwargs['task_id'])
        form.save()
        return redirect(
            'appeal:task_card',
            appeal_id=self.kwargs['appeal_id'],
            task_id=self.kwargs['task_id']
        )


class ReportCard(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Report
    template_name = 'appeal/report_card.html'
    fields = '__all__'
    pk_url_kwarg = 'report_id'
    context_object_name = 'report'
    permission_required = ['appeal.view_report', 'appeal.change_report']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appeal_id'] = self.kwargs['appeal_id']
        context['task_id'] = self.kwargs['task_id']
        context['report_id'] = self.kwargs['report_id']
        return context


class ReportDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Report
    template_name = 'appeal/appeal_confirm_action.html'
    pk_url_kwarg = 'report_id'
    permission_required = ['appeal.delete_report']

    def get_success_url(self):
        return reverse(
            'appeal:task_card',
            kwargs={
                'appeal_id': self.kwargs['appeal_id'],
                'task_id': self.kwargs['task_id'],
            }
        )
