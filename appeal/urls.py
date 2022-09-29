from django.urls import path

from .views import *

app_name = 'appeal'

urlpatterns = [
    path('create_appeal/',
         CreateAppeal.as_view(), name='create_appeal'),
    path('<int:appeal_id>/',
         AppealCard.as_view(), name='appeal_card'),
    path('<int:appeal_id>/delete',
         AppealDelete.as_view(), name='appeal_delete'),


    path('<int:appeal_id>/create_task',
         CreateTask.as_view(), name='create_task'),
    path('<int:appeal_id>/task/<int:task_id>/',
         TaskCard.as_view(), name='task_card'),
    path('<int:appeal_id>/task/<int:task_id>/delete',
         TaskDelete.as_view(), name='task_delete'),

    path('<int:appeal_id>/create_answer',
         CreateAnswer.as_view(), name='create_answer'),
    path('<int:appeal_id>/answer/<int:answer_id>/',
         AnswerCard.as_view(), name='answer_card'),
    path('<int:appeal_id>/answer/<int:answer_id>/delete',
         AnswerDelete.as_view(), name='answer_delete'),

    path('<int:appeal_id>/task/<int:task_id>/create_report',
         CreateReport.as_view(), name='create_report'),
    path('<int:appeal_id>/task/<int:task_id>/report/<int:report_id>',
         ReportCard.as_view(), name='report_card'),
    path('<int:appeal_id>/task/<int:task_id>/report/<int:report_id>/delete',
         ReportDelete.as_view(), name='report_delete'),
]
