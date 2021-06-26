from django.urls import path

from .views import WorkshopView, WorkshopItems, TagView

urlpatterns = [
    path('', WorkshopView.as_view(), name='workshop'),
    path('tags/', TagView.as_view(), name='tag'),
    path('items/', WorkshopItems.as_view(), name='workshop_items'),
]
