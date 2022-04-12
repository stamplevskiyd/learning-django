from django import forms
from .models import Tag
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):
    #title = forms.CharField(max_length=50)
    #slug = forms.CharField(max_length=50)

    #title.widget.attrs.update({'class': 'form-control'})
    #slug.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }


    def clean_slug(self):
        """Очистка от некорректных slug.

        Приведем к нижнему регистру и плюс запретим
        создавать с именем create, чтобы не было конфликта,
        расписанного в blog.urls.py и запретим дубли
        clean_title -> чистили бы заголовок. Стандартное название
        """

        new_slug = self.cleaned_data['slug'].lower()  # если дошли до сюда, в словаре точно
        # такое есть
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}"" slug already'.format(new_slug))

        return new_slug


    #def save(self):  # у ModelForm есть встроенный. А так каждый раз будет создаваться метод
    #    new_tag = Tag.objects.create(
    #        title=self.cleaned_data['title'],
    #        slug=self.cleaned_data['slug']
    #    )
    #    return new_tag
