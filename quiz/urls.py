from django.conf.urls import url

from .views import QuizView, QuizQuestionView

urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/', QuizQuestionView.as_view(), name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/', QuizView.as_view(), name='quiz_map'),
]
