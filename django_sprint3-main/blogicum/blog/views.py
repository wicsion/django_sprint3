from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.utils import timezone


from .models import Post, Category


def index(request):

    posts = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': posts,
    }

    return render(request, 'blog/index.html', context)


def category_posts(request, slug):

    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = category.post_set.filter(
        pub_date__lte=now(),
        is_published=True
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts,

    }

    return render(request, 'blog/category.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location')
        .filter(is_published=True)
        .filter(category__is_published=True)
        .filter(pub_date__lte=timezone.now()),
        pk=pk
    )

    context = {
        'post': post,
    }

    return render(request, 'blog/detail.html', context)
