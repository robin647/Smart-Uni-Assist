from rest_framework import generics, status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
import pandas as pd
from django.contrib.auth.models import User
from .serializers import ResultSerializer, UserSerializer, CourseSerializer, ReminderSerializer
from .models import Result, User, Course, Reminder, CSESkillDevelopmentCourse


GRADE_MAP = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'D': 1.0, 'F': 0.0,
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_recommendations(request):
    user = request.user
    results = Result.objects.filter(user=user)
    
    # Step 1: Collect result data
    data = []
    for r in results:
        grade_val = GRADE_MAP.get(r.grade, 0.0)
        data.append({'course': r.course.name, 'grade': grade_val})
    
    df = pd.DataFrame(data)

    # Step 2: Weak subjects (grade below 2.5)
    weak_courses = df[df['grade'] < 2.5]['course'].tolist()
    strong_courses = df[df['grade'] >= 3.0]['course'].tolist()

    # Step 3: Match with skill courses
    skill_courses = list(CSESkillDevelopmentCourse.objects.values_list('course_name', flat=True))
    
    # Suggest skill courses based on weaknesses
    suggestions = []
    for course in weak_courses:
        if 'Programming' in course:
            suggestions += [c for c in skill_courses if 'Python' in c or 'Web' in c]
        elif 'Math' in course or 'Calculus' in course:
            suggestions += [c for c in skill_courses if 'Data Analysis' in c or 'Statistics' in c]
        elif 'Physics' in course:
            suggestions += [c for c in skill_courses if 'Simulation' in c or 'Robotics' in c]

    # Remove duplicates and fallback if none
    suggestions = list(set(suggestions))
    if not suggestions:
        suggestions = list(skill_courses[:5])

    enrolled_courses = list(Course.objects.filter(user=user).values_list('name', flat=True))

    return Response({
        'user': user.username,
        'enrolled_courses': enrolled_courses,
        'retake_suggestions': weak_courses,
        'future_suggestions': suggestions,
    })


#  User Info View (for Dashboard)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'student_id': user.student_id,
        'email': user.email
    })

#  Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#  Login View using student_id
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        student_id = request.data.get('student_id')
        password = request.data.get('password')

        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid student ID'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'student_id': user.student_id
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Create new Course (for logged-in user)
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#  Create new Reminder (for logged-in user)
class ReminderCreateView(generics.CreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#  List only user's Courses
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)

#  List only user's Reminders
class ReminderListView(generics.ListAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
    
    
class ResultListCreateUpdateView(generics.ListCreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResultUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)

class CourseExcelUploadView(APIView):
    def post(self, request):
        excel_file = request.FILES.get('file')

        if not excel_file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                username = row['Username']
                user = User.objects.filter(username=username).first()
                if not user:
                    continue  
                Course.objects.create(
                    user=user,
                    name=row['Course Name'],
                    code=row['Course Code'],
                    teacher=row['Teacher']
                )

            return Response({"message": "Courses imported successfully!"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class ResultExcelUploadView(APIView):
    def post(self, request):
        excel_file = request.FILES.get('file')

        if not excel_file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                course_name = row['course_name']
                grade = row['grade']
                comment = row['comment']

                course = Course.objects.filter(name=course_name).first()
                if not course:
                    continue 

                Result.objects.create(
                    user=request.user,  
                    course=course,
                    grade=grade,
                    comment=comment
                )

            return Response({"message": "Results imported successfully!"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ResultAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get results for the logged-in user
        results = Result.objects.filter(user=request.user)
        
        # Serialize the results
        result_data = ResultSerializer(results, many=True).data
        
        return Response(result_data)

