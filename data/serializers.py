
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from .models import CustomUser
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Hide password in responses

    class Meta:
        model = User
        fields = [ 'username', 'fullname', 'password','role','first_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Hash password automatically
        return user

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
        
        
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'role':user.role,
                'first_name':user.first_name
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials") 



class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = '__all__'



class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class RecentVistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentVists
        fields = '__all__' 

# PatientsUnder a certain doctor
class PatientConsultingDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = '__all__'

class PatientWithFollowupSerializer(serializers.ModelSerializer):
    followups = serializers.SerializerMethodField()

    class Meta:
        model = PatientInfo
        fields = ['CrNo', 'Name', 'Age', 'Gender', 'Occupation', 'ConsultingDoctor', 'Diagnosis', 'FirstVisit', 'followups']

    def get_followups(self, obj):
        followups = RecentVists.objects.filter(CrNo=obj.CrNo)
        return RecentVistsSerializer(followups, many=True).data

#Doctor Name Serializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name']
        
        
        
        