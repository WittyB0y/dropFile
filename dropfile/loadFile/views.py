import os
from django.views.generic import ListView
from .models import files
from django.db.models import F
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import uuid
from django.views.static import serve
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from user.models import photo


@csrf_protect
def load_data(request):
    db = files.objects.latest('id')
    if request.method == 'POST' and request.FILES and request.user.is_authenticated:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        slug = uuid.uuid4()
        print(uploaded_file)
        data_type = str(uploaded_file)[str(uploaded_file).rfind('.'):]
        filename = fs.save(f'{slug}{data_type}', uploaded_file)
        from_user = request.META
        uploaded_file_obj = files.objects.create(
            file=filename,
            name=uploaded_file.name,
            content_type=uploaded_file.content_type,
            configdata=from_user['HTTP_USER_AGENT'],
            ipdata=from_user['REMOTE_ADDR'],
            slug=slug,
            userid=request.user,
        )
        return redirect(f'/{uploaded_file_obj.slug}')
    return render(request, 'loadFile/mainpage_end.html', {'lastdata': db})


class loadFile(ListView):
    model = files
    context_object_name = 'post'
    template_name = 'loadFile/endpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        data = files.objects.filter(slug=self.kwargs['slug']).update(seen=F('seen') + 1)
        if data < 1:
            raise Http404
        return files.objects.filter(slug=self.kwargs['slug'])


def download_file(request, slugy):
    try:
        uploaded_file = files.objects.get(slug=slugy)
        files.objects.filter(slug=slugy).update(downloded=F('downloded') + 1)
        file_path = uploaded_file.file.path
        return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
    except files.DoesNotExist:
        raise Http404


class myfiles(ListView):
    model = files
    context_object_name = 'posts'
    template_name = 'loadFile/myfiles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return files.objects.filter(userid=self.request.user)


def error_404_view(request, exception):
    return render(request, 'loadFile/404.html', status=404)
