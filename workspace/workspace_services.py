from appeal.models import Appeal, Task


def get_table_data_for_user(user):
    if user.groups.filter(name='administrator').exists():
        data = Appeal.objects.all().select_related('CategoryValue', 'AppealStatus')
        table_head = 'ID', 'Заголовок', 'Дата отправки', 'Статус', 'Категория'
        header = 'Входящие обращения'
        return data, table_head, header

    elif user.groups.filter(name='executor').exists():
        data = Task.objects.filter(UserExecutor=user)
        table_head = ('ID', 'Содержание', 'Дата постановки', 'Статус')
        header = 'Задачи'
        return data, table_head, header
    else:
        return None
