from django.shortcuts import render, redirect
from django.core.files import File

import os
import requests
from io import BytesIO
from PIL import Image

from .models import ImageModel
from .forms import UploadImgForm, ChangeImgSizeForm
from django.conf import settings


def index(request):
    """
    Берет весь список изображений из SQLite DB и отправляет на выход

    :param request:
    :return:
    """
    template_name = 'upload_img/index.html'
    images = ImageModel.objects.all()
    context = {'images': images, 'media_url': settings.MEDIA_URL}
    return render(request, template_name=template_name, context=context)


def upload_img_form(request):
    """
    url_img - способ добавление через url
    desktop_img - способ добавление через desktop
    Через POST добавления изображения в SQLite DB, и сохраняение файла изображения в папку media.
    Валидация полей формы UploadImgForm

    :param request:
    :return:
    """
    template_name = 'upload_img/upload.html'
    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            url_img = form.cleaned_data['url_img']
            desktop_img = form.cleaned_data['desktop_img']
            img_model = ImageModel()
            if url_img:
                img_name = os.path.basename(url_img)
                try:
                    headers = {
                        "User-Agent": "MyAppAgent/1.0",
                        "Accept": "*/*"
                    }
                    resp = requests.get(url_img, headers=headers)
                    if resp.status_code not in range(200, 209):
                        error_message = 'По указанному пути, страница не найдена.'
                        return render(request, template_name=template_name,
                                      context={'UploadImgForm': form, 'error_message': error_message})
                    fp = BytesIO()
                    fp.write(resp.content)
                    img_model.image.save(img_name, File(fp))
                    return redirect(f'/image/{img_model.pk}')
                except:
                    error_message = 'По указанному пути, отсутствует изображения.'
                    return render(request, template_name=template_name,
                                  context={'UploadImgForm': form, 'error_message': error_message})
            elif desktop_img:
                img_model.image = form.cleaned_data['desktop_img']
                img_model.save()
                return redirect(f'/image/{img_model.pk}')
    else:
        form = UploadImgForm()
    return render(request, template_name=template_name, context={'UploadImgForm': form})


def change_size_from(request, imguuid):
    """
    Через GET получение значений width и height и изменение размера изображения.

    :param request:
    :param imguuid:
    :return:
    """
    template_name = 'upload_img/image.html'
    image_data = ImageModel.objects.get(pk=imguuid)
    request_data = request.GET
    form = ChangeImgSizeForm(request.GET)
    context = {
        'media_url': settings.MEDIA_URL,
        'image_data': image_data,
        'ChangeImgSizeForm': form
    }

    if form.is_valid():
        img = Image.open(f'.{settings.MEDIA_URL}{image_data.image}')
        width = request_data.get('width', img.width)
        height = request_data.get('height', img.height)

        if not width:
            width = img.height
        if not height:
            height = img.height

        width = abs(int(width))
        height = abs(int(height))

        img.thumbnail((width, height), Image.ANTIALIAS)
        img.save(f'.{settings.MEDIA_URL}{image_data.image}')

        return render(request, template_name=template_name, context=context)
    else:
        return render(request, template_name=template_name, context=context)
