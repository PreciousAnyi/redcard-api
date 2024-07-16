from django.urls import path
from .views import UpcomingExamsView, PastExamsView, CardsView, RedCardView, RedCardByInvigilatorView
from .views import StudentThresholdListView, StudentThresholdDetailView, RedCardByStudentView
from .views import BlacklistView, DeleteRedcardView

urlpatterns = [
    path('upcoming_exams/', UpcomingExamsView.as_view(), name='upcoming-exams'),
    path('past_exams/', PastExamsView.as_view(), name='past-exams'),
    path('cards/', CardsView.as_view(), name='cards'),
    path('redcards/', RedCardView.as_view(), name='redcards'),
    path('thresholds/', StudentThresholdListView.as_view(), name='student-threshold-list'),
    path('thresholds/<str:user>/', StudentThresholdDetailView.as_view(), name='student-threshold-detail'),
    path('redcards/student/<str:personnel_no>/', RedCardByStudentView.as_view(), name='redcard-list-by-student'),
    path('redcards/invigilator/<str:personnel_no>/', RedCardByInvigilatorView.as_view(), name='redcard-list-by-invigilator'),
    path('blacklist/', BlacklistView.as_view(), name='blacklist'),
    path('redcards/<int:pk>/', DeleteRedcardView.as_view(), name='delete_redcard'),
]