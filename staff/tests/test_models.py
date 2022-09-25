from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group


class WorkerModelTestCase(TestCase):
    def setUp(self):
        self.admin1 = get_user_model().objects.create_user(
            username='test_admin1',
            password='test_pw'
        )
        self.group1 = Group.objects.create(
            name='administrator'
        )
        self.group1.user_set.add(self.admin1)

    def test_get_absolute_url(self):
        staff_url = f"/staff/{self.admin1.pk}"
        self.assertEqual(staff_url, self.admin1.get_absolute_url())

