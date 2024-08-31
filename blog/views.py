from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import (Blog, Tag, Category)

# Create your views here.
def home(request):
    blogs = Blog.objects.order_by('-created_date')[:5]
    tags = Tag.objects.order_by('-created_date')
    
    context = {
        "blogs":blogs,
        "tags":tags
    }

    return render(request, 'pages/home.html', context=context)

def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')


    context = {
        "blogs":blogs,
        "tags":tags,
        "paginator": paginator
    }
    return render(request, 'pages/blogs.html', context=context)

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:4]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 5)
    all_blogs = Blog.objects.order_by('-created_date')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        
        return redirect('blogs')

    context ={
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs,
        "queryset": queryset
    }

    return render(request, 'pages/category_blogs.html', context=context)


# def tag_blogs(request, slug):
#     tag = get_object_or_404(Tag, slug=slug)
#     queryset = tag.tag_blogs.all()
#     tags = Tag.objects.order_by('-created_date')[:4]
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 2)
#     all_blogs = Blog.objects.order_by('-created_date')[:5]

#     try:
#         blogs = paginator.page(page)
#     except EmptyPage:
#         blogs = paginator.page(1)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#         return redirect('blogs')

#     context ={
#         "blogs": blogs,
#         "tags": tags,
#         "all_blogs": all_blogs
#     }

#     return render(request, 'category_blogs.html', context=context)

def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id = blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:4]


    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags
    }
    return render(request, 'pages/blogDetails.html', context=context)
