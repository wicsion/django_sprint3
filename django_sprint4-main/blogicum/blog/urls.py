from django.urls import path, include
from django.contrib.auth.views import LogoutView  # Добавлен импорт для LogoutView
from .views import (
    register, create_post, edit_post, delete_post, add_comment,
    index, category_posts, post_detail, profile_view
)

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category_posts, name='category_posts'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', register, name='register'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:pk>/edit/', edit_post, name='edit_post'),
    path('posts/<int:pk>/delete/', delete_post, name='delete_post'),
    path('posts/<int:pk>/comment/', add_comment, name='add_comment'),  # Исправлено
    path('profile/<str:username>/', profile_view, name='profile'),  # Добавлен маршрут для профиля
    path('logout/', LogoutView.as_view(), name='logout'),  # Добавлен маршрут для logout
]
