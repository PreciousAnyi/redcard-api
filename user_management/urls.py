from django.urls import path
from .views import RegisterInvigilatorView, RegisterStudentView, LoginView, LogoutView

urlpatterns = [
    path('auth/register/invigilator', RegisterInvigilatorView.as_view(), name='register_invigilator'),
    path('auth/register/student', RegisterStudentView.as_view(), name='register_student'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]