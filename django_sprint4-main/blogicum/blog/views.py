from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

POSTS_LIMIT = 5


def get_base_post_queryset():
    """Возвращает базовый QuerySet для постов с необходимыми связями."""
    return (
        Post.objects.select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now()
        )
    )


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница с последними публикациями."""
    posts = get_base_post_queryset()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """Страница с публикациями определённой категории."""
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = get_base_post_queryset().filter(category=category)
    return render(request, 'blog/category.html', {'category': category, 'post_list': posts})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Страница с детальной информацией о публикации."""
    post = get_object_or_404(get_base_post_queryset(), pk=pk)

    # Если POST-запрос, обрабатываем добавление комментария
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=pk)  # Перенаправляем на текущую страницу

    else:
        comment_form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': comment_form})  # Передаем форму комментария


def register(request: HttpRequest) -> HttpResponse:
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_post(request: HttpRequest) -> HttpResponse:
    """Создание нового поста."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего поста."""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление поста."""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """Страница профиля пользователя."""
    profile_user = get_object_or_404(User, username=username)
    posts = get_base_post_queryset().filter(author=profile_user)
    return render(request, 'blog/profile.html', {'profile_user': profile_user, 'post_list': posts})


@login_required
def add_comment(request, pk):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)

    return redirect('blog:post_detail', pk=pk)