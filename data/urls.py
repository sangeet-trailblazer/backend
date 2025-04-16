from django.urls import path
from .views import *
from . import views



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
    

    # Doctor's name list 
      path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    
    
    # # MedicalHistory URLspath('patients/', views.PatientInfoListCreate.as_view(), name='patient_list_create'),
    #  path('medical-history/', views.MedicalHistoryListCreate.as_view(), name='medical_history_list_create'),
    #  path('medical-history/<int:patient_id>/', views.MedicalHistoryDetail.as_view(), name='medical_history_detail'),
     
    #   path('blood-reports/', views.BloodReportList.as_view(), name='blood-report-list'),  # GET, POST
    # path('blood-reports/<int:patient_id>/', views.BloodReportDetail.as_view(), name='blood-report-detail'),  # GET, PUT, DELETE

    # # CurrentSymptoms URLs
    # path('current-symptoms/', views.CurrentSymptomsList.as_view(), name='current-symptoms-list'),  # GET, POST
    # path('current-symptoms/<int:patient_id>/', views.CurrentSymptomsDetail.as_view(), name='current-symptoms-detail'),  # GET, PUT, DELETE
   

    


]