import news.models
from api.models import idPhone
from user.models import photo
from django.contrib.auth.models import User as user
from loadFile.models import files, FileAccess, renderData
from rest_framework import serializers


class DataUploadFiles(serializers.ModelSerializer):
    class Meta:
        model = files
        fields = '__all__'


class serializerNews(serializers.ModelSerializer):
    class Meta:
        model = news.models.news
        fields = ('title', 'text', 'link', 'image',)


class filesSerializer(serializers.ModelSerializer):
    userid = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = files
        fields = ('id', 'slug', 'createdAt', 'downloded', 'seen', 'file', 'name', 'content_type', 'userid', 'access')


class PhotoSerializer(serializers.ModelSerializer):
    userid = serializers.CurrentUserDefault

    class Meta:
        model = photo
        fields = ('photo', 'userid',)


class RenderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = renderData
        fields = ['number', 'fileLink']


class FileSerializer(serializers.ModelSerializer):
    userid = PhotoSerializer(source='userid.photo')

    class Meta:
        model = files

        fields = ('name', 'userid',)


# class FileSerializerLoads(serializers.ModelSerializer):
#     lookingSeeUsers = serializers.SerializerMethodField()
#
#     def get_lookingSeeUsers(self, obj):
#         return UserSerializer(obj.lookingSeeUsers.all(), many=True).data
#
#     class Meta:
#         model = FileAccess
#         fields = ('id', 'lookingSeeUsers', 'createdAt', 'existBefore', 'seenUser', 'webSee', 'userSeeClient', 'amount', 'fileid')

class FileSerializerLoads(serializers.ModelSerializer):
    lookingSeeUsers = serializers.SerializerMethodField()

    def get_lookingSeeUsers(self, obj):
        users = obj.lookingSeeUsers.all()
        user_data = []
        for user_obj in users:
            photo_url = user_obj.photo.photo.url
            user_data.append({
                'id': user_obj.id,
                'username': user_obj.username,
                'photo_url': photo_url
            })
        return user_data

    class Meta:
        model = FileAccess
        fields = ('id', 'lookingSeeUsers', 'createdAt', 'existBefore', 'seenUser', 'webSee', 'userSeeClient', 'amount', 'fileid')



class FileAccessSerializer(serializers.ModelSerializer):
    fileid = FileSerializer()
    renderdata = RenderDataSerializer(many=True, source='fileid.renderdata_set')

    class Meta:
        model = FileAccess
        # 'lookingSeeUsers',
        fields = ['createdAt', 'existBefore', 'userSeeClient', 'fileid', 'renderdata']


class userdata(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('last_login', 'username', 'date_joined',)


class myUploadedFiles(serializers.ModelSerializer):
    class Meta:
        model = files
        fields = ('slug', 'userid_id', 'access', 'created_at', 'content_type', 'name', 'seen', 'downloaded',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    # devid = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = user
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        data_creted = user.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return data_creted


class idPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = idPhone
        fields = ('devid', 'userid',)


class FileSerializerUPLOAD(serializers.ModelSerializer):
    class Meta:
        model = files
        fields = '__all__'

    id = serializers.IntegerField(read_only=True)
    file = serializers.FileField()
    uploaded_at = serializers.DateTimeField(read_only=True)
    userid = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        validated_data['userid'] = self.context['request'].user
        return super().create(validated_data)
