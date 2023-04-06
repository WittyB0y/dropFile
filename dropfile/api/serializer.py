from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from loadFile.models import files


class filesSerializer(serializers.ModelSerializer):
    userid = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = files
        fields = '__all__'