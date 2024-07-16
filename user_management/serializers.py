from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Invigilator, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['personnel_no', 'fullname', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class InvigilatorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Invigilator
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        invigilator = Invigilator.objects.create(user=user)
        return invigilator

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'department', 'threshold']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

class LoginSerializer(serializers.Serializer):
    personnel_no = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        personnel_no = data.get('personnel_no')
        password = data.get('password')

        if personnel_no and password:
            user = authenticate(username=personnel_no, password=password)
            data['user'] = user
        else:
            raise serializers.ValidationError('Personnel_no and password needed')
        return data