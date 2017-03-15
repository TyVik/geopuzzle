from django.conf.urls import url, include

from quiz import views

area_patterns = [
    url(r'^(?P<pk>\d+)/giveup/', views.giveup, name='quiz_giveup'),
    url(r'^(?P<pk>\d+)/check/', views.check, name='quiz_question'),
]

urlpatterns = [
    url(r'', include(area_patterns)),
    url(r'^questions/(?P<name>[a-zA-Z0-9]+)', views.questions, name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9]+)', views.quiz, name='quiz_quiz'),
]
