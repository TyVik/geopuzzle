from django.conf.urls import url

from .views import WorkshopView, WorkshopItems, suggest, TagView

urlpatterns = [
    url(r'^$', WorkshopView.as_view(), name='workshop'),
    url(r'^suggest/$', suggest, name='workshop_suggest'),
    url(r'^tags/$', TagView.as_view(), name='tag'),
    url(r'^items/$', WorkshopItems.as_view(), name='workshop_items'),
]
