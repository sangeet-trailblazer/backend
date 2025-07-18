from django.urls import path,include
from ai_model import views
urlpatterns = [
    path('generate/', views.generate_response, name='generate_response'),
     path('auth/', include('data.urls')),
     path('api/', include('data.urls')),

]

