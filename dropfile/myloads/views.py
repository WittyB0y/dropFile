from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from user.models import photo as bd_photo

@csrf_protect
def get_files(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        photo = bd_photo.objects.get(userid=request.user)
        print(photo.photo)
    return render(request, 'myloads/myfiles.html', {'photo':photo})