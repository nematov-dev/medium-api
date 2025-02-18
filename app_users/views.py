from django.contrib.auth import get_user_model
from django.template.context_processors import request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, UserSerializer, UpdatePasswordSerializer
from .models import VerificationCode
from .utils import send_verification_email
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            # Foydalanuvchi mavjudligini tekshirish
            if User.objects.filter(email=email).exists():
                return Response({"error": "Bu email allaqachon ro‘yxatdan o‘tgan"}, status=status.HTTP_400_BAD_REQUEST)

            # Foydalanuvchini yaratish (faol emas)
            user = serializer.save()

            # Email kodini yuborish
            send_verification_email(email)

            return Response({"message": "Tasdiqlash kodi emailga yuborildi"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailApiView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email va kod talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verification_code = VerificationCode.objects.get(email=email, code=code)

            if not verification_code.is_valid():
                return Response({"error": "Kod eskirgan yoki noto‘g‘ri"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

            # Kodni o‘chirish
            verification_code.delete()

            return Response({"message": "Email tasdiqlandi"}, status=status.HTTP_200_OK)

        except VerificationCode.DoesNotExist:
            return Response({"error": "Kod noto‘g‘ri yoki mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                return Response({"error": "Email tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })


        return Response({"error": "Username yoki parol noto‘g‘ri"}, status=status.HTTP_401_UNAUTHORIZED)

class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdatePasswordSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=200)

        return Response(serializer.errors, status=400)



class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return  Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self,request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





