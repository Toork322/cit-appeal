from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from .models import Worker
from .forms import WorkerRegisterForm
from .staff_services import get_other_workers, register_worker


class Workers(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'staff/workers.html'
    context_object_name = 'data'
    extra_context = {
        'table_head': ['ID пользователя', 'Имя пользователя', 'Группа']
    }
    permission_required = ['staff.view_worker']

    def get_queryset(self):
        return get_other_workers(self.request.user.pk)


class WorkerPageUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['username', 'password', 'groups', 'is_superuser']
    pk_url_kwarg = 'worker_id'
    template_name = 'staff/worker_page.html'
    permission_required = ['staff.change_worker']
    success_url = reverse_lazy('staff:workers')


class WorkerPageDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'staff/worker_page_delete.html'
    success_url = reverse_lazy('staff:workers')
    pk_url_kwarg = 'worker_id'
    permission_required = ['staff.delete_worker']


class RegisterWorker(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = WorkerRegisterForm
    template_name = 'staff/register_worker.html'
    permission_required = ['staff.add_worker']

    def form_valid(self, form):
        register_worker(form)
        return redirect("staff:workers")


class LoginWorker(LoginView):
    form_class = AuthenticationForm
    template_name = 'staff/login_worker.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('workspace')


@login_required(login_url='/staff/login/')
def logout_worker(request):
    logout(request)
    return redirect('staff:login_worker')
