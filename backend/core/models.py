# backend/core/models.py
from django.db import models
from users.models import CustomUser

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class UserFile(models.Model):
    FILE_TYPES = (
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('WORD', 'Word'),
        ('TXT', 'Text'),
        ('OTHER', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_directory_path)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.original_filename
    
    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.name
        super().save(*args, **kwargs)