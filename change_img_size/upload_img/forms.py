from django import forms

from utils.module import is_url_image, check_url_status


class UploadImgForm(forms.Form):
    """
    Форма добавления изобрвжения по URL ссылке или через desktop
    """
    url_img = forms.CharField(label='Ссылка', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Введите URL'}))
    desktop_img = forms.ImageField(label='Файл', required=False)

    def clean(self):
        url_img = self.cleaned_data.get('url_img')
        desktop_img = self.cleaned_data.get('desktop_img')

        if url_img and desktop_img:
            raise forms.ValidationError('Пожалуйста, выберите только один способ добавления изображения.')

        if url_img and not is_url_image(url_img):
            raise forms.ValidationError('Просьба проверить, в указанном URL изображения не найдена.')


class ChangeImgSizeForm(forms.Form):
    """
    Форма изменения размера изображения
    """
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    def clean(self):
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if not width and not height:
            raise forms.ValidationError('Пожалуйста, необходимо заполнить одно или два поля числовыми значениями.')
