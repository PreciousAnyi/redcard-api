from rest_framework import serializers
from .models import Card, RedCard, Exam, Blacklist
from user_management.models import Student, Invigilator

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'description', 'points']

class RedcardSerializer(serializers.ModelSerializer):
    student_reg_no = serializers.CharField(write_only=True)
    invigilator_no = serializers.CharField(write_only=True)
    offence = serializers.CharField(write_only=True)
    
    invigilator_name = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    
    class Meta:
        model = RedCard
        fields = ['id', 'student_reg_no', 'invigilator_no', 'offence', 'points', 'invigilator_name', 'issued_at']
    
    def get_invigilator_name(self, obj):
        return obj.issued_by.user.fullname

    def get_points(self, obj):
        return obj.card.points


    def create(self, validated_data):
        student_reg_no = validated_data.pop('student_reg_no')
        invigilator_no = validated_data.pop('invigilator_no')
        offence = validated_data.pop('offence')

        student = Student.objects.get(user__personnel_no=student_reg_no)
        invigilator = Invigilator.objects.get(user__personnel_no=invigilator_no)
        card = Card.objects.get(description=offence)

        redcard = RedCard.objects.create(student=student, card=card, issued_by=invigilator, **validated_data)
        return redcard


class ExamSerializer(serializers.ModelSerializer):
    invigilators_names = serializers.SerializerMethodField()
    exam_date = serializers.SerializerMethodField()
    exam_time = serializers.SerializerMethodField()

    class Meta:
        model = Exam 
        fields = ['id', 'title', 'exam_date', 'exam_time', 'invigilators_names']
    
    def get_exam_date(self, obj):
        return obj.date.date()

    def get_exam_time(self, obj):
        return obj.date.time()
    
    def get_invigilators_names(self, obj):
        return [invigilator.user.fullname for invigilator in obj.invigilators.all()]

class BlacklistSerializer(serializers.ModelSerializer):
    student_reg_no = serializers.SerializerMethodField()
    class Meta:
        model = Blacklist
        fields = ['id', 'student_name', 'student_reg_no', 'threshold']
    
    def get_student_reg_no(self, obj):
        return obj.student.user.personnel_no

class StudentThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'threshold']