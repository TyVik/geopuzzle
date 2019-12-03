from django.conf.urls import url

from .views import questions, quiz

urlpatterns = [
    url(r'^(?P<name>[a-zA-Z0-9_]+)/questions/', questions, name='quiz_questions'),
    url(r'^(?P<name>[a-zA-Z0-9_]+)/', quiz, name='quiz_map'),
]
