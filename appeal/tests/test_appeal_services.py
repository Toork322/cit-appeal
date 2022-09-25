from django.test import TestCase

from appeal.appeal_services import get_appeal_from_id, predict_category
from appeal.models import Appeal, Category, Status


class GeneralFuncsTestCase(TestCase):
    def setUp(self):
        self.category_ad = Category.objects.create(
            CategoryValue='Реклама'
        )
        self.status_waiting = Status.objects.create(
            StatusValue='В ожидании'
        )

    def test_get_appeal_from_id(self):
        appeal = Appeal.objects.create(
            FirstName='Ivan',
            SecondName='Ivanov',
            ThirdName='Ivanovich',
            SocialStatus='Пенсия',
            PhoneNumber='123',
            EmailAddress='asd@asd.asd',
            PhysicalAddress='asdasd',
            AppealContent='asdasdasd',
            CategoryValue=self.category_ad,
            AppealStatus=self.status_waiting
        )
        self.assertEqual(get_appeal_from_id(appeal.pk), appeal)


class TextProcessingTestCase(TestCase):
    def test_predict_category(self):
        text = 'Необходимо тщательно мытье лестницы на всех этажах с применением чистящих средств'
        self.assertTrue(isinstance(predict_category(text), int))
