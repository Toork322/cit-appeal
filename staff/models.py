from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Worker(AbstractUser):

    def get_absolute_url(self):
        return reverse('staff:worker_page', kwargs={'worker_id': self.pk})
