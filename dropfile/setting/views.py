from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import EditUserForm, EditUserPhoto
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from user.models import photo as bd_photo
from loadFile.models import files as bd_file
from loadFile.models import dataCounter
from django.core.files.storage import FileSystemStorage
import uuid


@method_decorator(csrf_protect, name='dispatch')
class settingData(DetailView):
    model = User
    template_name = 'setting/setting.html'

    def get(self, request, pk):
        data = {}
        try:
            photo = bd_photo.objects.get(userid=request.user.id)
        except bd_photo.DoesNotExist:
            photo = {'photo': 'media/users/mainphoto/user.jpg'}
        data['photo'] = photo
        if request.user.is_authenticated and pk == request.user.id:
            countFile = dataCounter.objects.filter(userid=request.user.id)
            data['countFile'] = countFile
            try:
                data['total'] = countFile.allowedFiles - countFile.amount_of_files
            except AttributeError:
                data['total'] = 100
            return render(request, 'setting/setting.html', context=data)
        else:
            if not request.user.is_authenticated:
                return redirect('login')
            return redirect('settings', pk=request.user.id)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@csrf_protect
@login_required
def delete_profile(request, pk):
    username = request.user.username
    date = User.objects.get(id=request.user.id).date_joined
    try:
        photo = bd_photo.objects.get(userid=request.user.id)
    except bd_photo.DoesNotExist:
        photo = {'photo': 'media/users/mainphoto/user.jpg'}
    if request.method == 'POST':
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            return redirect('home')
        else:
            return HttpResponseBadRequest('Invalid password')
    else:
        return render(request, 'setting/delete_profile.html',
                      context={'photo': photo, 'username': username, 'date': date})


@csrf_protect
@login_required
def delete_all_files(request, pk):
    try:
        photo = bd_photo.objects.get(userid=request.user.id)
    except bd_photo.DoesNotExist:
        photo = {'photo': 'media/users/mainphoto/user.jpg'}
    if request.method == 'POST':
        password = request.POST['password']
        user = authenticate(request=request, username=request.user.username, password=password)
        if user is not None:
            files = iter(bd_file.objects.filter(userid=request.user.id))
            for file in files:
                file.delete()
            return redirect('settings', pk=request.user.id)
        else:
            return HttpResponseBadRequest('Invalid password')
    else:
        return render(request, 'setting/delete_files.html', context={'photo': photo})


@csrf_protect
def change_password(request, pk):
    if pk == request.user.id:
        if request.method == 'POST' and pk == request.user.id:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings', pk=request.user.id)
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'setting/change_password.html', {
            'form': form
        })
    else:
        if request.user.is_authenticated:
            return redirect('settings', pk=request.user.id)
        return redirect('login')


class changeDetails(LoginRequiredMixin, FormView):
    form_class = EditUserForm
    template_name = 'setting/change_details.html'
    model = User
    success_url = 'home'

    def form_valid(self, form):
        if form.is_valid:
            data = User.objects.filter(id=self.request.user.id).update(
                email=self.request.POST.get('email'),
                first_name=self.request.POST.get('first_name'),
                last_name=self.request.POST.get('last_name')
            )
        return super().form_valid(form)


@csrf_protect
@login_required
def change_photo(request, pk):
    form = EditUserPhoto(request.POST, request.FILES)
    data = {'form': form}
    try:
        photo = bd_photo.objects.filter(userid=request.user.id)
    except:
        photo = {'photo': 'media/users/mainphoto/user.jpg'}
    data['photo'] = photo
    if request.method == 'POST' and request.FILES:
        if form.is_valid:
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage()
            slug = uuid.uuid4()
            data_type = str(uploaded_file)[str(uploaded_file).rfind('.'):]
            filename = fs.save(f'users/{request.user.id}/{slug}{data_type}', uploaded_file)
            photo.update(photo=f'media/{filename}')
    return render(request, 'setting/change_photo.html', context=data)
