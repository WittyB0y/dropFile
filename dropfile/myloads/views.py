from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from user.models import photo as bd_photo
from loadFile.models import files as bd_file
from django.http import HttpResponse

@csrf_protect
def get_files(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        photo = bd_photo.objects.get(userid=request.user)
        try:
            files = bd_file.objects.filter(userid=request.user)
            counter = files.count()
            lst_file = files[counter-1].created_at
        except:
            counter = 0
            lst_file = 'Загрузок не было'
    return render(request, 'myloads/myfiles.html', {'photo':photo, 'files':files, 'count':counter, 'lst_file':lst_file})


def delete_file(request, slug):
    if request.user.is_authenticated:
        try:
            file = bd_file.objects.get(slug=slug, userid=request.user)
            file.delete()
        except:
            pass
        finally:
            return redirect('myFiles')
    else:
        return redirect('home')