from rest_framework import serializers
from .models import Result, User, Course, Reminder

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'student_id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        return Course.objects.create(user=user, **validated_data)


class ReminderSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = Reminder
        fields = ['course', 'assignment_title', 'due_date']
        

    def create(self, validated_data):
        user = self.context['request'].user
        return Reminder.objects.create(user=user, **validated_data)

class ResultSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course.name')  # for display

    class Meta:
        model = Result
        fields = ['id', 'user', 'course', 'course_name', 'grade', 'comments']
        read_only_fields = ['user']
