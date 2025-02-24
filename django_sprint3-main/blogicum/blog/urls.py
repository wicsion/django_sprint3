from django.urls import path
from .views import index, category_posts, post_detail

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category_posts, name='category_posts'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),

]
