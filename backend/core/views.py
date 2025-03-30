# backend/core/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import UserFile
from .serializers import UserFileSerializer, FileUploadSerializer
import os
from datetime import datetime

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            filename = file.name
            file_ext = os.path.splitext(filename)[1].lower()
            
            file_type = 'OTHER'
            if file_ext == '.pdf':
                file_type = 'PDF'
            elif file_ext in ['.xls', '.xlsx']:
                file_type = 'EXCEL'
            elif file_ext == '.docx':
                file_type = 'WORD'
            elif file_ext == '.txt':
                file_type = 'TXT'
            
            user_file = UserFile.objects.create(
                user=request.user,
                file=file,
                original_filename=filename,
                file_type=file_type
            )
            
            return Response(UserFileSerializer(user_file).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListView(generics.ListAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserFile.objects.filter(user=self.request.user).order_by('-uploaded_at')

class FileDeleteView(generics.DestroyAPIView):
    queryset = UserFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserFile.objects.filter(user=self.request.user)

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Total files uploaded
        total_files = UserFile.objects.filter(user=request.user).count()
        
        # File type breakdown
        file_types = UserFile.objects.filter(user=request.user).values('file_type').annotate(count=Count('file_type'))
        
        # Files uploaded per day (last 7 days)
        from django.db.models.functions import TruncDate
        files_per_day = UserFile.objects.filter(
            user=request.user,
            uploaded_at__gte=datetime.now().date() - timedelta(days=7)
        ).annotate(date=TruncDate('uploaded_at')).values('date').annotate(count=Count('id')).order_by('date')
        
        return Response({
            'total_files': total_files,
            'file_types': list(file_types),
            'files_per_day': list(files_per_day),
        })