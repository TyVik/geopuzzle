from django.conf.urls import url, include

from quiz import views

urlpatterns = [
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)/', views.questions, name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)/', views.quiz, name='quiz_map'),
]
