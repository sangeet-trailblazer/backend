from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
def home(request):
    return HttpResponse("Welcome to the homepage!")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # App URL configs
    path('api/', include('data.urls')),
    path('api/', include('ai_model.urls')),

    # Access and Refesh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('auth/', include('data.urls')),
    path('api/', include('data.urls')),
    
    
]

