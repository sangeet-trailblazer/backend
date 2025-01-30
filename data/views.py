from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

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


# Create your views here.
