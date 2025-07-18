from django.urls import path,include
from .views import *
from . import views
from .views import forget_password
urlpatterns = [
    
     path('register/', UserRegisterAPIView.as_view(), name='register'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('login/', UserLoginView.as_view(), name='login'),
    

    # PatientInfo URLs
     path('patients/', views.PatientInfoListCreate.as_view(), name='patient_list_create'),
     path('patients/<int:pk>/', views.PatientInfoListCreate.as_view(), name='patient_detail'),
   
    # Patients under a doctor
    path('under/',views.get_patients_data,name='patients-consulting-one-doctor'),
    # Recent Visit Urls
    path('visits/', views.RecentVistsListCreateAPIView.as_view(), name='visits'),
    path('visits/<int:pk>/', views.RecentVistsListCreateAPIView.as_view(), name='visits'),
    path('visits/patch/<int:CrNo>/', views.RecentVistsListCreateAPIView.as_view(), name='visits'),
 
    #Diagnosis
    path('diagnosis/', DiagnosisCreateAPIView.as_view(), name='diagnosis-list-create'),
    path('diagnosis/<int:pk>/', DiagnosisCreateAPIView.as_view(), name='diagnosis-detail'),
    
    # Patient with followup serializer 
    path('patientfollowups/', PatientFollowupView.as_view(), name='patients-with-followups'),


      path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    # change Password path 
      path('password_change/', views.password_change, name='password_change'),
    # forgot Password 
      path('forget_password/', forget_password, name='forget_password'),
    #steps
      path('send-otp/', forget_password),
      path('verify-otp/', forget_password),
      path('reset-password/', forget_password),
      
      path('patients-by-doctor/', PatientsByDoctorView.as_view(), name='patients-by-doctor'),
]