# cit-appeal

python manage.py loaddata create_groups add_categories add_status_values

createsuperuser

python manage.py shell

from django.contrib.auth.models import Group

group = Group.objects.get(name='administrator') 

user = get_user_model().objects.get(pk=1)

group.user_set.add(user)