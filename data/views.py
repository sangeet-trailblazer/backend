from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

# 1.1 User Registration 

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#1.2 AllUserLogin 
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
  
        if valid:
            status_code = status.HTTP_200_OK
            userdetails=serializer.validated_data
            response = {
                'success': True,
            
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'authenticated_user':userdetails,
            }

            return Response(response, status=status_code)

class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Create a RefreshToken instance
                token = RefreshToken(refresh_token)
                
                # Blacklist the refresh token
                token.blacklist()
                
                return Response({'success': True,'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            except TokenError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Patient
class PatientInfoListCreate(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk=None):
        if pk:
            visits = PatientInfo.objects.filter(CrNo=pk)  # Fetch visits for a specific patient
            if not visits.exists():
                return Response({"error": "No recent visits found for this patient"}, status=status.HTTP_404_NOT_FOUND)
        else:
            visits = PatientInfo.objects.all()  # Fetch all visits
        
        serializer = PatientInfoSerializer(visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
   
    def post(self, request):
        serializer = PatientInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Triggers save method with Followup logic
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Diagnosis Views
class DiagnosisCreateAPIView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk=None):
        if pk:
            visits = Diagnosis.objects.filter(CrNo=pk)  # Fetch visits for a specific patient
            if not visits.exists():
                return Response({"error": "No recent visits found for this patient"}, status=status.HTTP_404_NOT_FOUND)
        else:
            visits = Diagnosis.objects.all()  # Fetch all visits
        
        serializer = DiagnosisSerializer(visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
   
    def post(self, request):
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Triggers save method with Followup logic
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Recent Visit 
class RecentVistsListCreateAPIView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk=None):
        if pk:
            visits = RecentVists.objects.filter(CrNo=pk)  # Fetch visits for a specific patient
            if not visits.exists():
                return Response({"error": "No recent visits found for this patient"}, status=status.HTTP_404_NOT_FOUND)
        else:
            visits = RecentVists.objects.all()  # Fetch all visits
        
        serializer = RecentVistsSerializer(visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def patch(self, request, CrNo=None):
        try:
            instance = RecentVists.objects.get(CrNo=CrNo)
        except RecentVists.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecentVistsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        serializer = RecentVistsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Triggers save method with Followup logic
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patients Under a doctor
@api_view(['GET'])
@permission_classes ([AllowAny])
def get_patients_data(request):
    
    # Extract the doctor's name from the request parameters
    doctor_name = request.GET.get('doctor_name', None)

    # If doctor_name is provided, filter patients by the doctor
    if doctor_name:
        patients = PatientInfo.objects.filter(ConsultingDoctor=doctor_name)
    else:
        # If no doctor_name is provided, fetch all patients
        patients = PatientInfo.objects.all()

    # Serialize the patients data
    patients_data = PatientConsultingDoctorSerializer(patients, many=True).data

    # Return the data as JSON
    return Response(patients_data)


# Patient With Followup serializer

class PatientFollowupView(APIView):
    permission_classes=(AllowAny,)
    def get(self, request):
        doctor_name = request.GET.get('doctor_name')
        if doctor_name:
            patients = PatientInfo.objects.filter(ConsultingDoctor=doctor_name)
        else:
            patients = PatientInfo.objects.all()

        serializer = PatientWithFollowupSerializer(patients, many=True)
        return Response(serializer.data)

#Docor Lists API View

class DoctorListView(APIView):
    permission_classes=(AllowAny,)
    def get(self, request):
        doctors = CustomUser.objects.filter(role='Doctor')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)













# # MedicalHistory Views

# class MedicalHistoryListCreate(APIView):
#     permission_classes=[AllowAny] 
#     def get(self, request):
#         medical_histories = MedicalHistory.objects.all()
#         serializer = MedicalHistorySerializer(medical_histories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MedicalHistorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MedicalHistoryDetail(APIView):
#     permission_classes = [AllowAny]

#     def get_object(self, patient_id):
#         # Return queryset of medical histories for the patient
#         return MedicalHistory.objects.filter(patient__Patientid=patient_id)

#     def get(self, request, patient_id):
#         # Get the medical history for the specific patient
#         medical_history = self.get_object(patient_id)
#         if medical_history.exists():  # Checking if there are any results
#             serializer = MedicalHistorySerializer(medical_history, many=True)
#             return Response(serializer.data)
#         return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, patient_id):
#         # Update the medical history of the specific patient
#         medical_history = self.get_object(patient_id)
#         if medical_history.exists():
#             serializer = MedicalHistorySerializer(medical_history, data=request.data, many=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, patient_id):
#         # Delete the medical history records of the specific patient
#         medical_history = self.get_object(patient_id)
#         if medical_history.exists():
#             medical_history.delete()
#             return Response({"message": "Medical history deleted successfully for this patient"}, status=status.HTTP_204_NO_CONTENT)
#         return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)
