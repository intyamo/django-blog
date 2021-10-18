from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Post


class HomePageView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "blog_post_list"


class PostDetailsView(DetailView):
    model = Post
    template_name = "post_details.html"


class PostCreateView(CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ["title", "author", "body"]


class PostUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
