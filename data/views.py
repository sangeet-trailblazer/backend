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

class PatientInfoListCreate(APIView):
    permission_classes=[AllowAny]  
    def get(self, request):
        patients = PatientInfo.objects.all()
        serializer = PatientInfoSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = PatientInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientInfoDetail(APIView):
    permission_classes=[AllowAny] 
    def get_object(self, pk):
        try:
            return PatientInfo.objects.get(Patientid=pk)
        except PatientInfo.DoesNotExist:
            return None

    def get(self, request, pk):
        patient = self.get_object(pk)
        if patient is not None:
            serializer = PatientInfoSerializer(patient)
            return Response(serializer.data)
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        patient = self.get_object(pk)
        if patient is not None:
            serializer = PatientInfoSerializer(patient, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        patient = self.get_object(pk)
        if patient is not None:
            patient.delete()
            return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)


# MedicalHistory Views

class MedicalHistoryListCreate(APIView):
    permission_classes=[AllowAny] 
    def get(self, request):
        medical_histories = MedicalHistory.objects.all()
        serializer = MedicalHistorySerializer(medical_histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicalHistoryDetail(APIView):
    permission_classes = [AllowAny]

    def get_object(self, patient_id):
        # Return queryset of medical histories for the patient
        return MedicalHistory.objects.filter(patient__Patientid=patient_id)

    def get(self, request, patient_id):
        # Get the medical history for the specific patient
        medical_history = self.get_object(patient_id)
        if medical_history.exists():  # Checking if there are any results
            serializer = MedicalHistorySerializer(medical_history, many=True)
            return Response(serializer.data)
        return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, patient_id):
        # Update the medical history of the specific patient
        medical_history = self.get_object(patient_id)
        if medical_history.exists():
            serializer = MedicalHistorySerializer(medical_history, data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, patient_id):
        # Delete the medical history records of the specific patient
        medical_history = self.get_object(patient_id)
        if medical_history.exists():
            medical_history.delete()
            return Response({"message": "Medical history deleted successfully for this patient"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Medical history not found for this patient"}, status=status.HTTP_404_NOT_FOUND)


class BloodReportList(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        blood_reports = BloodReport.objects.all()
        serializer = BloodReportSerializer(blood_reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BloodReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodReportDetail(APIView):
    permission_classes = (AllowAny, )

    def get_object(self, patient_id):
        try:
            return BloodReport.objects.filter(patient__Patientid=patient_id)
        except BloodReport.DoesNotExist:
            return None

    def get(self, request, patient_id):
        blood_report = self.get_object(patient_id)
        if blood_report.exists():
            serializer = BloodReportSerializer(blood_report, many=True)
            return Response(serializer.data)
        return Response({"error": "Blood report not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, patient_id):
        blood_report = self.get_object(patient_id)
        if blood_report.exists():
            serializer = BloodReportSerializer(blood_report, data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Blood report not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, patient_id):
        blood_report = self.get_object(patient_id)
        if blood_report.exists():
            blood_report.delete()
            return Response({"message": "Blood report deleted successfully for this patient"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Blood report not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

# CurrentSymptoms Views
class CurrentSymptomsList(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        current_symptoms = CurrentSymptoms.objects.all()
        serializer = CurrentSymptomsSerializer(current_symptoms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CurrentSymptomsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentSymptomsDetail(APIView):
    permission_classes = (AllowAny, )

    def get_object(self, patient_id):
        try:
            return CurrentSymptoms.objects.filter(patient__Patientid=patient_id)
        except CurrentSymptoms.DoesNotExist:
            return None

    def get(self, request, patient_id):
        current_symptoms = self.get_object(patient_id)
        if current_symptoms.exists():
            serializer = CurrentSymptomsSerializer(current_symptoms, many=True)
            return Response(serializer.data)
        return Response({"error": "Current symptoms not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, patient_id):
        current_symptoms = self.get_object(patient_id)
        if current_symptoms.exists():
            serializer = CurrentSymptomsSerializer(current_symptoms, data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Current symptoms not found for this patient"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, patient_id):
        current_symptoms = self.get_object(patient_id)
        if current_symptoms.exists():
            current_symptoms.delete()
            return Response({"message": "Current symptoms deleted successfully for this patient"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Current symptoms not found for this patient"}, status=status.HTTP_404_NOT_FOUND)
