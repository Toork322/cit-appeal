from django.urls import path

from .views import *

app_name = 'staff'

urlpatterns = [
    path('login/', LoginWorker.as_view(), name='login_worker'),
    path('logout/', logout_worker, name='logout_worker'),
    path('register/', RegisterWorker.as_view(), name='register_worker'),
    path('<int:worker_id>', WorkerPageUpdate.as_view(), name='worker_page'),
    path('<int:worker_id>/delete', WorkerPageDelete.as_view(), name='worker_page_delete'),
    path('', Workers.as_view(), name='workers')
]
