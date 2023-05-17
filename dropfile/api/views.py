import datetime
import os
import uuid

import pytz
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from loadFile.models import files, FileAccess
from .bill import extract_zip_file
from .models import idPhone
from .serializer import filesSerializer, userdata, myUploadedFiles, UserSerializer, idPhoneSerializer, \
    serializerNews, PhotoSerializer, RenderDataSerializer, FileAccessSerializer, DataUploadFiles, FileSerializerUPLOAD, \
     FileSerializerLoads
from rest_framework import generics, status
from user.models import photo
from django.contrib.auth.models import User as user
from loadFile.models import files, FileAccess
from news.models import news
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def upload_file(request):
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({'error': 'No file was submitted'}, status=status.HTTP_400_BAD_REQUEST)
    elif uploaded_file and uploaded_file.name[-4:].upper() == '.ZIP':
        new_name = f'{uuid.uuid4()}.zip'
        uploaded_file.name = new_name
        os.makedirs('media/data/', exist_ok=True)
        with open('media/data/' + new_name, 'wb') as f:
            f.write(uploaded_file.read())
        created_obj = files.objects.create(
            file=new_name,
            name=uploaded_file.name,
            content_type=uploaded_file.content_type,
            ipdata='127.0.0.1',
            slug=uuid.uuid4(),
            userid=request.user,
        )
        extract_zip_file(f'media/data/{new_name}', request.user, created_obj.id)
    else:
        return HttpResponse('Файл должен быть с расширением .zip')

    return Response({'success': True}, status=status.HTTP_201_CREATED)


# @csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def insertPermission(request):
    dataPost = request.data
    if request.method == 'POST':

        try:
            user1 = user.objects.get(username=dataPost['user'])
            file = files.objects.get(id=dataPost['fileid'], userid=request.user.id)
            new_time = datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=int(dataPost['time']))
            files_access = FileAccess.objects.create(fileid=file, existBefore=new_time)
            files_access.lookingSeeUsers.set([user1])
            files_access.save()
            return Response({'success': 'Права доступа успешно добавлены.'}, status=status.HTTP_201_CREATED)
        except user.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        except files.DoesNotExist:
            return Response({'error': 'Файл не найден.'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        file_id = request.headers.get('Fileid')
        file_access = FileAccess.objects.filter(fileid=file_id)
        serializer = FileSerializerLoads(file_access, many=True)
        return Response(serializer.data)


class newsAPI(generics.ListAPIView):
    queryset = news.objects.all().order_by('-id')
    serializer_class = serializerNews


class filesAPIList(generics.ListAPIView):
    """show all files that used loaded"""
    serializer_class = filesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return files.objects.filter(userid=self.request.user).order_by('-id')


class filesAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = files.objects.all()
    serializer_class = filesSerializer


class filesAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = files.objects.all()
    serializer_class = filesSerializer


class getProfilePhotoURL(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        data = photo.objects.filter(userid=self.request.user)
        return data


class getUserData(generics.ListAPIView):
    serializer_class = userdata
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return user.objects.filter(id=self.request.user.id)


class myFiles(generics.ListAPIView):
    serializer_class = myUploadedFiles
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return files.objects.filter(userid=self.request.user)


class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDeviceID(generics.RetrieveUpdateAPIView):
    serializer_class = idPhoneSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return idPhone.objects.filter(userid=self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.devid is not None:
            return Response({'error': 'Cannot update non-null devid field.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().update(request, *args, **kwargs)


class ImageUploadView(viewsets.ModelViewSet):
    # queryset = photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return photo.objects.filter(userid=self.request.user.id)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid() and self.request.user.id == int(kwargs.get("pk")):
            photo_file = serializer.validated_data['photo']
            photo_file.name = f'profile_photo_{uuid.uuid4()}.png'

            photo_dir = f'media/users/{kwargs.get("pk")}/profile/'
            os.makedirs(photo_dir, exist_ok=True)
            for file in os.listdir(photo_dir):
                if file.startswith('profile_photo_') and os.path.isfile(os.path.join(photo_dir, file)):
                    os.remove(os.path.join(photo_dir, file))

            photo_path = photo_dir + photo_file.name
            print(photo_path)
            with open(photo_path, 'wb') as f:
                f.write(photo_file.read())

            # Обновляем путь к фотографии в базе данных
            serializer.save(photo=photo_path)

            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileAccessList(generics.ListAPIView):
    serializer_class = FileAccessSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = FileAccess.objects.filter(
            Q(lookingSeeUsers=user),
            # exist_before__gte=datetime.datetime.now()
        ).select_related('fileid__userid').prefetch_related('fileid__renderdata_set')

        return queryset
