from django.conf.urls import url

from quiz import views

urlpatterns = [
    url(r'^questions/(?P<name>[a-zA-Z0-9_]+)/', views.questions, name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/', views.quiz, name='quiz_map'),
]
