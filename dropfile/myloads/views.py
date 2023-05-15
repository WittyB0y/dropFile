from django.shortcuts import render, redirect
from user.models import photo as bd_photo
from loadFile.models import files as bd_file
from loadFile.models import dataCounter
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.db.models import F


@method_decorator(csrf_protect, name='dispatch')
class GetFilesView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            data = {}
            files = bd_file.objects.filter(userid=request.user)
            counter = files.count()
            lst_file = files[counter - 1].createdAt if counter > 0 else 'Загрузок не было'
            try:
                photo = bd_photo.objects.get(userid=request.user)
            except bd_photo.DoesNotExist:
                photo = {'photo': 'media/users/mainphoto/user.jpg'}
            except:
                counter = 0
                files = ''
            data.update({'photo': photo, 'files': files, 'count': counter, 'lst_file': lst_file})
            return render(request, 'myloads/myfiles.html', context=data)


def delete_file(request, slug):
    if request.user.is_authenticated:
        try:
            file = bd_file.objects.get(slug=slug, userid=request.user)
            file.delete()
        except:
            pass
        finally:
            dataCounter.objects.filter(userid=request.user.id).update(amount_of_files=F('amount_of_files') - 1)
            return redirect('myFiles')
    else:
        return redirect('home')


def change_accsses(request, slug, bool_type):
    if request.user.is_authenticated:
        try:
            file = bd_file.objects.filter(slug=slug, userid=request.user)
            if bool_type == 'True':
                file.update(access=False)
            elif bool_type == 'False':
                file.update(access=True)
        except:
            pass
        finally:
            return redirect('myFiles')
    else:
        return redirect('login')
