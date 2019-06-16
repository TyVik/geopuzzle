from django.conf.urls import url

from .views import WorkshopView, WorkshopItems

urlpatterns = [
    url(r'^$', WorkshopView.as_view(), name='workshop'),
    url(r'^items/$', WorkshopItems.as_view(), name='workshop_items'),
]
