from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView


class settingData(CreateView):
    model = User
    template_name = 'setting/setting.html'
    fields = ['username','password']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context