from django.db import models

import uuid


class ImageModel(models.Model):
    """
    Модель данных изображения
    uuid - Идентификатор
    image - путь к файлу изображения
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=False)

    class Meta:
        db_table = 'upload_images'

