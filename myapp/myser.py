#导包
from rest_framework import serializers
from .models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'