from django.shortcuts import get_object_or_404

from .models import Answer


def get_answers_for_appeal(appeal_id):
    return Answer.objects.filter(CurrentAppeal__pk=appeal_id).select_related('CurrentAppeal')


