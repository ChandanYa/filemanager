# backend/core/serializers.py
from rest_framework import serializers
from .models import UserFile

class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['id', 'original_filename', 'file_type', 'uploaded_at', 'file']
        read_only_fields = ['original_filename', 'file_type', 'uploaded_at']

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()