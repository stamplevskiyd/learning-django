from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):

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


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        return new_slug
