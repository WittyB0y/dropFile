import os
from django.views.generic import ListView
from .models import files
from django.db.models import F
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import uuid
from django.views import View
from django.utils.decorators import method_decorator
from django.views.static import serve
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from user.models import photo as bd_photo
from datetime import datetime

@method_decorator(csrf_protect, name='dispatch')
class LoadDataView(View):

    def get(self, request):
        try:
            db = files.objects.latest('id')
        except Exception as e:
            print(e)
            db = 'Загрузок ещё не было'
        data = {
                'lastdata': db, 
                'title': 'Файлообменник | Главная', 
            }
        if request.user.is_authenticated:
            try:
                photo = bd_photo.objects.get(userid=request.user)
            except bd_photo.DoesNotExist:
                photo = {'photo':'media/users/mainphoto/catty.jpg'}
            data['photo'] = photo
            return render(request, 'loadFile/file_upload.html', context=data)
        return render(request, 'loadFile/file_upload.html', context=data)
        
        

    def post(self, request):
        if request.method == 'POST' and request.FILES and request.user.is_authenticated:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            slug = uuid.uuid4()
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
        return redirect('home')




class loadFile(ListView):
    model = files
    context_object_name = 'post'
    template_name = 'loadFile/files_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                photo = bd_photo.objects.get(userid=self.request.user)
            except bd_photo.DoesNotExist:
                photo = {'photo':'media/users/mainphoto/catty.jpg'}
            context['photo'] = photo
        return context

    def get_queryset(self, *args, **kwargs):
        data = files.objects.filter(slug=self.kwargs['slug'])
        if len(data) < 1:
            raise Http404
        elif data[0].access == True and data[0].userid.id != self.request.user.id:
            raise Http404
        else:
            data.update(seen=F('seen') + 1)
            return data


def download_file(request, slugy):
    try:
        uploaded_file = files.objects.get(slug=slugy)
        print(type(uploaded_file.access), type(uploaded_file.userid.id),type(request.user.id))
        if (uploaded_file.access == True and uploaded_file.userid.id == request.user.id) or (uploaded_file.access == False):
            files.objects.filter(slug=slugy).update(downloded=F('downloded') + 1)
            file_path = uploaded_file.file.path
            return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
        else:
            raise Http404
    except files.DoesNotExist:
        raise Http404


class myfiles(ListView):
    model = files
    context_object_name = 'posts'
    template_name = 'loadFile/myfiles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            photo = bd_photo.objects.get(userid=self.request.user)
        except bd_photo.DoesNotExist:
            photo = {'photo':'media/users/mainphoto/catty.jpg'}
        context['photo'] = photo
        return context

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return files.objects.filter(userid=self.request.user)


def error_404_view(request, exception):
    return render(request, 'loadFile/404.html', status=404)