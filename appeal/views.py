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

# def report_card(request, appeal_id, task_id, report_id):
#     if request.method == 'POST':
#         if request.POST.get('report_action') == 'save_changes':
#             post_data = request.POST.copy()
#             form = ReportGeneralForm(post_data, instance=get_report_from_id(report_id))
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse('Изменения сохранены.')
#             else:
#                 return HttpResponse('Форма недействительна. Повторите попытку.')
#
#         elif request.POST.get('report_action') == 'delete_report':
#             get_report_from_id(report_id).delete()
#             return HttpResponse('Задача удалена.')
#
#         else:
#             return HttpResponse('Ошибка.')
#     else:
#         form = ReportGeneralForm(instance=get_report_from_id(report_id))
#         context = {
#             'form': form,
#             'report_id': report_id
#         }
#         return render(request, 'appeal/report_card.html', context=context)

# def create_appeal(request):
#     if request.method == 'POST':
#         form = AppealCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('Обращение отправлено.')
#     else:
#         form = AppealCreateForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'appeal/create_appeal.html', context=context)


# def create_task(request, appeal_id):
#     if request.method == 'POST':
#         form = TaskCreateForm(request.POST)
#         if form.is_valid():
#             form.instance.CurrentAppeal = Appeal.objects.get(pk=appeal_id)
#             form.save()
#         return redirect('appeal:appeal_card', appeal_id=appeal_id)
#
#     else:
#         form = TaskCreateForm()
#         context = {
#             'form': form,
#             'appeal_id': appeal_id
#             }
#         return render(request, 'appeal/create_task.html', context=context)


# def create_answer(request, appeal_id):
#     if request.method == 'POST':
#         form = AnswerGeneralForm(request.POST)
#         if form.is_valid():
#             form.instance.CurrentAppeal = Appeal.objects.get(pk=appeal_id)
#             form.save()
#             return redirect('appeal:appeal_card', appeal_id=appeal_id)
#         else:
#             return HttpResponse('Форма недействительна. Повторите попытку.')
#     else:
#         form = AnswerGeneralForm()
#         context = {
#             'form': form,
#             'appeal_id': appeal_id
#         }
#         return render(request, 'appeal/create_answer.html', context=context)


# def create_report(request, appeal_id, task_id):
#     if request.method == 'POST':
#         form = ReportGeneralForm(request.POST)
#         if form.is_valid():
#             form.instance.CurrentTask = Task.objects.get(pk=task_id)
#             form.save()
#             return redirect('appeal:task_card', task_id=task_id, appeal_id=appeal_id)
#         else:
#             return HttpResponse('Форма недействительна. Повторите попытку.')
#     else:
#         form = ReportGeneralForm()
#         context = {
#             'form': form,
#             'task_id': task_id
#         }
#         return render(request, 'appeal/create_report.html', context=context)


# def appeal_card(request, appeal_id):
#     if request.method == 'POST':
#         if request.POST.get('appeal_action') == 'save_changes':
#             post_data = request.POST.copy()
#             form = AppealCardForm(post_data, instance=get_appeal_from_id(appeal_id))
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse('Изменения сохранены.')
#             else:
#                 return HttpResponse('Форма недействительна. Повторите попытку.')
#         elif request.POST.get('appeal_action') == 'delete_appeal':
#             get_appeal_from_id(appeal_id).delete()
#             return HttpResponse('Обращение удалено.')
#         else:
#             return HttpResponse('Ошибка.')
#
#     form = AppealCardForm(instance=get_appeal_from_id(appeal_id))
#     context = {
#         'appeal': get_appeal_from_id(appeal_id),
#         'tasks': get_tasks_for_appeal(appeal_id),
#         'answers': get_answers_for_appeal(appeal_id),
#         'form': form
#     }
#     return render(request, 'appeal/appeal_card.html', context=context)


# def task_card(request, appeal_id, task_id):
#     if request.method == 'POST':
#         if request.POST.get('task_action') == 'save_changes':
#             post_data = request.POST.copy()
#             form = TaskCardForm(post_data, instance=get_task_from_id(task_id))
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse('Изменения сохранены.')
#             else:
#                 return HttpResponse('Форма недействительна. Повторите попытку.')
#
#         elif request.POST.get('task_action') == 'delete_task':
#             get_task_from_id(task_id).delete()
#             return HttpResponse('Задача удалена.')
#
#         else:
#             return HttpResponse('Ошибка.')
#
#     else:
#         form = TaskCardForm(instance=get_task_from_id(task_id))
#         context = {
#             'reports': get_reports_for_task(task_id),
#             'form': form,
#             'task_id': task_id,
#             'appeal_id': appeal_id
#             }
#         return render(request, 'appeal/task_card.html', context=context)


# def answer_card(request, appeal_id, answer_id):
#     if request.method == 'POST':
#         if request.POST.get('answer_action') == 'save_changes':
#             post_data = request.POST.copy()
#             form = AnswerGeneralForm(post_data, instance=get_answer_from_id(answer_id))
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse('Изменения сохранены.')
#             else:
#                 return HttpResponse('Форма недействительна. Повторите попытку.')
#
#         elif request.POST.get('answer_action') == 'delete_answer':
#             get_answer_from_id(answer_id).delete()
#             return HttpResponse('Задача удалена.')
#
#         else:
#             return HttpResponse('Ошибка.')
#     else:
#         form = AnswerGeneralForm(instance=get_answer_from_id(answer_id))
#         context = {
#             'form': form,
#             'answer_id': answer_id
#         }
#         return render(request, 'appeal/answer_card.html', context=context)
