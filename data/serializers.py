from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login  
from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        if not username or not password :
            raise serializers.ValidationError("all fields are required")
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        # try:
        #     CaptchaStore.objects.get(hashkey=hashkey, response=response.strip().lower())
        # except CaptchaStore.DoesNotExist:
        #     raise serializers.ValidationError("Invalid captcha")
        
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials") 



class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class BloodReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodReport
        fields = '__all__'

class CurrentSymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentSymptoms
        fields = '__all__'
class BloodReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodReport
        fields = '__all__'

class CurrentSymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentSymptoms
        fields = '__all__'       