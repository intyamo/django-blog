from django.urls import path

from .views import (
    HomePageView,
    PostDetailsView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("post/new", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailsView.as_view(), name="post_details"),
    path("post/<int:pk>/edit", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post_delete"),
]
