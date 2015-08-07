from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Blog

def index(request):
    blog_list = Blog.objects.order_by('-date')

    paginator = Paginator(blog_list, 5)
    page = request.GET.get('page')
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        blog = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.num_pages
        blog = paginator.page(page)

    next_page = False
    previous_page = False
    page = int(page)
    if blog.has_next():
        next_page = '?page=' + str(page+1)
    if blog.has_previous():
        previous_page = '?page=' + str(page-1)

    return render(request, 'templates/blog.html', {'blog': blog, 'page': page, 'next_page': next_page, 'previous_page': previous_page})

def article(request, post_id):
    post = Blog.objects.get(url=post_id)
    return render(request, 'templates/article.html', {'post': post})