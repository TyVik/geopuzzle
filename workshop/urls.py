from django.conf.urls import url

from .views import WorkshopView, WorkshopItems, suggest

urlpatterns = [
    url(r'^$', WorkshopView.as_view(), name='workshop'),
    url(r'^suggest/$', suggest, name='workshop_suggest'),
    url(r'^items/$', WorkshopItems.as_view(), name='workshop_items'),
]
