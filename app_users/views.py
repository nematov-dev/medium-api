from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from app_users.serializes import RegisterSerializers

class RegisterApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializers

    def post(self,request):
        pass



