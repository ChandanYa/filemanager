from django.contrib import admin
from django.urls import path, include, re_path  # Added re_path import
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    path('', TemplateView.as_view(template_name='index.html')),
]

from rest_framework.authtoken.views import obtain_auth_token
from users.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserUpdateView,
    AddressListView,
    AddressDetailView
)
from core.views import (
    FileUploadView,
    FileListView,
    FileDeleteView,
    DashboardStatsView
)

# API URL patterns
api_patterns = [
    # Authentication
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile-update'),
    
    # Addresses
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    
    # Files
    path('files/upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileDeleteView.as_view(), name='file-delete'),
    
    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),  # All API routes under /api/
    
    # Frontend catch-all route (must be last)
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]

# Static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)