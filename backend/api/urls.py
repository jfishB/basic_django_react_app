from django.urls import path
from . import views

urlpatterns = [
    path("jump-videos/", views.JumpVideoViewSet.as_view(), name="jump-video-list"),
]