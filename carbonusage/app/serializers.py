from rest_framework import serializers
from .models import User, Usage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = '__all__'


