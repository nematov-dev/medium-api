from rest_framework import serializers


class RegisterSerializers(serializers.Serializer):
    first_name = serializers.CharField()
    las_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()