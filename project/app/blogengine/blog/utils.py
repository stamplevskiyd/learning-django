from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *

class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})


    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():  # одновременно и "создание" и проверка
            new_obj = bound_form.save()  # сохраним
            return redirect(new_obj)  # многофункциональная и полезная функция
        return render(request, self.template, context={'form': bound_form})
