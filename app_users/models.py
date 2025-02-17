from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now


from app_common.models import BaseModel


class ProfileModel(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='profiles',validators=[FileExtensionValidator(allowed_extensions=['png','jpg','heic'])])
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class VerificationCode(models.Model):
    email = models.EmailField(unique=True)  # Foydalanuvchi emaili
    code = models.CharField(max_length=6)  # 6 xonali kod
    created_at = models.DateTimeField(auto_now_add=True)  # Kod yaratilgan vaqt
    expires_at = models.DateTimeField()  # Amal qilish muddati

    def save(self, *args, **kwargs):
        # Kodni 5 daqiqadan keyin o'chadigan qilib saqlaymiz
        self.expires_at = now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        """Kodning amal qilish muddatini tekshirish"""
        return now() < self.expires_at

    def __str__(self):
        return f"{self.email} - {self.code} (Expires: {self.expires_at})"

