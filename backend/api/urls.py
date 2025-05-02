from django.urls import path
from .views import RegisterView, LoginView,CourseCreateView, ReminderCreateView, CourseListView, ReminderListView, ResultListCreateUpdateView, ResultUpdateView,get_user_info
from .views import CourseExcelUploadView,ResultAnalysisView,course_recommendations
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('courses/create/', CourseCreateView.as_view()),
    path('reminders/', ReminderListView.as_view()),
    path('reminders/create/', ReminderCreateView.as_view()),
    path('user-info/', get_user_info),
    path('course-recommendations/', course_recommendations),
    path('results/', ResultListCreateUpdateView.as_view(), name='results'),
    path('results/<int:pk>/', ResultUpdateView.as_view(), name='result-update'),
    path('upload-courses/', CourseExcelUploadView.as_view(), name='upload-courses'),
    path('api/result-analysis/', ResultAnalysisView.as_view(), name='result-analysis'),
    
]
