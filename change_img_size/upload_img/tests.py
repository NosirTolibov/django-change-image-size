from django.test import TestCase, Client, SimpleTestCase
from upload_img.models import ImageModel


class MainTestCase(TestCase):
    def setUp(self):
        ImageModel.objects.create(uuid='458858c5d9034c63b63566f0ee8e57a2', image='images/2021/04/08/moscow_city.png')
        ImageModel.objects.create(uuid='adb9ad52cd1047a39778f3be9e9ecf94', image='images/2021/04/08/ny_city.png')

    def test_access_page(self):
        c = Client()

        # index page
        response = c.get('')
        self.assertEqual(response.status_code, 200)

        # upload page
        response = c.get('/upload/')
        self.assertEqual(response.status_code, 200)

        # image page
        query = ImageModel.objects.all()
        self.assertNotEqual(len(query), 0)

        for q in query:
            response = c.get(f'/image/{q.uuid}/')
            self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        c = Client()
        query = ImageModel.objects.all()

        response = c.get('')
        images_list = response.context['images']
        # Добавленные изображения
        self.assertIsNotNone(images_list)
        # Все изображения страницы
        self.assertEqual(len(query), len(images_list))

