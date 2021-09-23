from .models import BlogModel
from collections import UserDict
from os import read
from typing import Collection
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
import json


class Blogserializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        pass

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Ensure this field has more than 6 characters")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__exact=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
