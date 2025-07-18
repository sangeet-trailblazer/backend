#django related
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

import random
import traceback
from datetime import timedelta
#rest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
#jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
#twilio
from twilio.rest import Client

from .models import *
from .models import PatientInfo
from .serializers import (
    UserLoginSerializer,
    UserSerializer,
    DiagnosisSerializer,
    PatientInfoSerializer,
    RecentVistsSerializer,
    PatientConsultingDoctorSerializer,
    PatientWithFollowupSerializer,
    DoctorSerializer
)
User = get_user_model()
#twilio credentials
TWILIO_SID = 'AC535c1243b951118b2b0fba1405d29912'
TWILIO_AUTH_TOKEN = 'b825d358503389cbd133c0dfa0a423e2'
TWILIO_PHONE_NUMBER = '+16083446821'

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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

#Doctor Lists API View

class DoctorListView(APIView):
    permission_classes=(AllowAny,)
    def get(self, request):
        doctors = CustomUser.objects.filter(role='Doctor')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

#function for password_change
@api_view(['POST']) #method =POST because we are changing it
@authentication_classes([JWTAuthentication]) #uses Jwt
@permission_classes([IsAuthenticated])#only for selected users
def password_change(request):#function
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # for any empty space
    if not all([old_password, new_password, confirm_password]):
        return Response(
            {"error": "All fields are required."},#if left empty
            status=status.HTTP_400_BAD_REQUEST #400= error
        )

    #Check if old password matches
    if not user.check_password(old_password):# verification whether the old password is correct or not
        return Response(
            {"error": "Old password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST #for wrong password
        )

    # checking if both the passwords matched or not new & confirm
    if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update password and saving it
    user.set_password(new_password)
    user.save()

    return Response(
        {"message": "Password changed successfully."},
        status=status.HTTP_200_OK
    )
    return Response(
        {"message": "Password changed successfully! You can now log in with the new password."},
        status=status.HTTP_200_OK
    )
#function generating 4 digit OTP Using  random function
def generate_otp():
    return str(random.randint(1000, 9999))

# forget Password
@api_view(['POST'])# atlast password is reset so POST
@permission_classes([AllowAny])# any visitor can use this feature
def forget_password(request): #function
    username = request.data.get('username')
    step = request.data.get('step')
    print(f"Step received: {step}")

    if step == "send_otp":# step1
        raw_phone = request.data.get('phone', '')
        request_phone = '+91' + raw_phone[-10:]
        print(f"Username: {username}, Phone: {request_phone}")

        try:
            user = User.objects.get(username=username)
            db_phone = user.phonenumber
            normalized_db_phone = '+91' + db_phone[-10:]

            if request_phone != normalized_db_phone:
                return Response({"error": "Username and phone number do not match."}, status=400)

            otp = generate_otp()
            print(f"Generated OTP for {username}: {otp}")#using the random functon inside the generate OTP function

            # Save OTP to otpstore database
            OTPStore.objects.create(
                username=username,
                otp=otp,
                verified=False,
                timestamp=timezone.now()# latest password to be checked for the user
            )

            #sending OTP via Twilio
            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"Your OTP is {otp}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=request_phone
                )
                print(f"OTP sent. Twilio SID: {message.sid}")
            except Exception as e:
                print("Twilio error:", e)
                return Response({"error": f"Failed to send SMS: {str(e)}"}, status=500)

            return Response({"message": "OTP sent"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    elif step == "verify_otp": #step 2
        otp = request.data.get('otp', '').strip()# for any blank spaces we use 
        expiration_time = timezone.now() - timedelta(minutes=1)

        try:
            # Delete expired OTPs
            OTPStore.objects.filter(username=username, timestamp__lt=expiration_time).delete()

            # Get most recent valid OTP
            record = OTPStore.objects.filter(
                username=username,
                timestamp__gte=expiration_time
            ).order_by('-timestamp').first()

            if not record:
                return Response({"error": "OTP not found or expired"}, status=404)

            if record.otp == otp:
                record.verified = True
                record.save()
                return Response({"message": "OTP verified"})
            else:
                return Response({"error": "Incorrect OTP"}, status=400)

        except Exception as e:
            print("OTP verify error:", e)
            return Response({"error": "Something went wrong while verifying OTP"}, status=500)

    elif step == "reset_password":
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        try:
            record = OTPStore.objects.filter(username=username).order_by('-timestamp').first()
            if not record or not record.verified:
                return Response({"error": "OTP not verified"}, status=400)

            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Delete all OTPs for this user after one gets verified.
            OTPStore.objects.filter(username=username).delete()

            return Response({"message": "Password reset successful"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response({"error": "Invalid step"}, status=400)
class PatientsByDoctorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor_name = request.GET.get('doctor_name')
        if not doctor_name:
            return Response({"error": "Doctor name is required"}, status=status.HTTP_400_BAD_REQUEST)

        patients = PatientInfo.objects.filter(ConsultingDoctor=doctor_name)
        serializer = PatientInfoSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)