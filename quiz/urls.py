from django.conf.urls import url

from quiz import views

urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/', views.questions, name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/', views.quiz, name='quiz_map'),
]
