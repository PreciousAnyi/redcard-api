from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import StudentSerializer, InvigilatorSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

# Views here.

class RegisterInvigilatorView(generics.CreateAPIView):
    serializer_class = InvigilatorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    errors.append({'field': field, 'message': message})
            return Response({'errors': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        invigilator = serializer.save()
        invigilator_data = serializer.data

        return Response({
            'status': 'success',
            'message': 'Invigilator registration successful',
            'data': invigilator_data
        }, status=status.HTTP_201_CREATED)

class RegisterStudentView(generics.CreateAPIView):
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    errors.append({'field': field, 'message': message})
            return Response({'errors': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        student = serializer.save()
        student_data = serializer.data

        return Response({
            'status': 'success',
            'message': 'Student registration successful',
            'data': student_data
        }, status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    errors.append({'field': field, 'message': message})
            return Response({
                'errors': errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            # Proceed with authentication logic
            user = serializer.validated_data['user']
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'user': {
                        'personnel_no': user.personnel_no,
                        'fullname': user.fullname,
                    }
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'Bad request',
                'message': 'Authentication failed',
                'statusCode': status.HTTP_401_UNAUTHORIZED
            })
        
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,) 
    serializer_class = serializers.Serializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                return Response({
                    'status': 'Bad request',
                    'message': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'status': 'success',
                'message': 'Logout successful'
            }, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({
                'status': 'Bad request',
                'message': 'Failed to logout',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)