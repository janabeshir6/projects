from django.contrib import admin, messages 
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import authentication views

from django.contrib.auth import views as auth_views
from django.urls import path, include
from library.views import CustomLoginView  # Ensure this matches your app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),  # Include library app URLs
    path('accounts/login/', CustomLoginView.as_view(template_name='library/login.html'), name='login'),  # Custom login view
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout view
    path('accounts/', include('django.contrib.auth.urls')),  # Password management routes
]
