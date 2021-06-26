from django.urls import path

from .views import QuizView, QuizQuestionView

urlpatterns = [
    path('<name>/questions/', QuizQuestionView.as_view(), name='quiz_questions'),
    path('<name>/', QuizView.as_view(), name='quiz_map'),
]
