from rest_framework import generics
from django.utils import timezone
from .models import Exam, Card, RedCard, Blacklist
from user_management.models import Student, Invigilator
from .serializers import ExamSerializer, CardSerializer, RedcardSerializer, BlacklistSerializer, StudentThresholdSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from user_management.permission import IsInvigilator, IsStudent, IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class UpcomingExamsView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [IsAdmin|IsInvigilator|IsStudent]
    authentication_classes = (JWTAuthentication,)  


    def get_queryset(self):
        return Exam.objects.filter(date__gte=timezone.now())

class PastExamsView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [IsAdmin|IsInvigilator|IsStudent]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Exam.objects.filter(date__lt=timezone.now())

class CardsView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdmin|IsInvigilator]
    authentication_classes = (JWTAuthentication,)

class RedCardView(APIView):
    permission_classes = [IsAdmin|IsInvigilator]
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        redcards = RedCard.objects.all()
        serializer = RedcardSerializer(redcards, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
    operation_description="Create a new red card",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'student_reg_no': openapi.Schema(type=openapi.TYPE_STRING),
            'invigilator_no': openapi.Schema(type=openapi.TYPE_STRING),
            'offence': openapi.Schema(type=openapi.TYPE_STRING),
            # Add more properties as needed
        },
    ),
    responses={201: RedcardSerializer},
)
    def post(self, request, *args, **kwargs):
        serializer = RedcardSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RedCardByStudentView(APIView):
    permission_classes = [IsAdmin|IsStudent]
    authentication_classes = (JWTAuthentication,)
    def get(self, request, personnel_no, *args, **kwargs):
        student = get_object_or_404(Student, user__personnel_no=personnel_no)
        redcards = RedCard.objects.filter(student=student)
        serializer = RedcardSerializer(redcards, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class RedCardByInvigilatorView(generics.ListAPIView):
    serializer_class = RedcardSerializer
    permission_classes = [IsAdmin|IsInvigilator]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        personnel_no = self.kwargs['personnel_no']
        invigilator = get_object_or_404(Invigilator, user__personnel_no=personnel_no)
        return RedCard.objects.filter(issued_by=invigilator)

class StudentThresholdListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentThresholdSerializer
    permission_classes = [IsAdmin]
    authentication_classes = (JWTAuthentication,)

class StudentThresholdDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentThresholdSerializer
    permission_classes = [IsAdmin|IsStudent]
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'user'

class BlacklistView(generics.ListAPIView):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer
    permission_classes = [IsAdmin]
    authentication_classes = (JWTAuthentication,)

class DeleteRedcardView(generics.DestroyAPIView):
    queryset = RedCard.objects.all()
    serializer_class = RedcardSerializer
    permission_classes = [IsInvigilator]
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        operation_description="Remove an already assigned red card",
        responses={
            204: 'No Content',
            404: 'Not Found'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            redcard = self.get_object()
            redcard.delete()
            return Response({'detail': 'Card deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except RedCard.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
