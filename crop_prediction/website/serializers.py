from rest_framework import serializers

from .models import users_model

class user_serializer(serializers.ModelSerializer):

    class Meta:
        model = users_model
        fields = ['email','password']