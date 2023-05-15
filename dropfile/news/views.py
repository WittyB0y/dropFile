from django.shortcuts import render
from django.views.generic import ListView


class NewsPage(ListView):

    def get(self, request):
        return render(request, 'news/NewsPage.html')

