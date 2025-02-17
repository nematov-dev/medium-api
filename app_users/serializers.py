from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VerificationCode
import random
import string

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Parollar mos kelmadi")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_active = False  # Email tasdiqlanguncha foydalanuvchini nofaol qoldiramiz
        user.save()
        return user

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))
