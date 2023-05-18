from django.shortcuts import render, redirect
from blogs.models import Blog, Post
from blogs.forms import CreateBlogForm, CreatePostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@login_required
def home_page(request):
    if request.method == 'GET':
        blogs = Blog.objects.select_related('owner').order_by('-created_at')
        return render(request, 'blogs/index.html', {'blogs': blogs})
    else:
        return redirect('/auth/login/')


@user_passes_test(lambda u: u.is_staff)
def create_blog_page(request):
    if request.method == 'GET':
        form = CreateBlogForm()
        return render(request, 'blogs/create-blog.html', {'form': form})

    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            blog = Blog(title=title, description=description, owner=request.user)
            blog.save()
            return redirect('/')

    return redirect('/auth/login/')


def blog_details_page(request, pk):
    if request.method == 'GET':
        form = CreatePostForm()
        blog = Blog.objects.get(id=pk)
        posts = Post.objects.filter(blog_id=pk)
        return render(request, 'blogs/blog-details.html', {'blog': blog, 'user': request.user, 'form': form,
                                                           'posts': posts})


@user_passes_test(lambda u: u.is_staff)
def blog_details_page_for_staff(request, pk):
    if request.method == 'GET':
        form = CreatePostForm()
        blog = Blog.objects.get(id=pk)
        posts = Post.objects.filter(blog_id=pk)

        return render(request, 'blogs/blog-details.html',
                      {'blog': blog, 'user': request.user, 'form': form, 'posts': posts})


@user_passes_test(lambda u: u.is_staff)
def delete_blog_page(request, pk):
    if request.method == 'GET':
        form = CreatePostForm()
        blog = Blog.objects.get(id=pk)
        posts = Post.objects.filter(blog_id=pk)
        return render(request, 'blogs/blog-details.html',
                      {'blog': blog, 'user': request.user, 'form': form, 'posts': posts})

    if request.method == 'POST':
        try:
            blog = Blog.objects.get(id=pk)
            if request.user.id == blog.owner.id:
                blog.delete()
        except Blog.DoesNotExist:
            pass

    return redirect('/')


@user_passes_test(lambda u: u.is_staff)
def create_blogs_post(request, pk):
    if request.method == 'POST':
        blog = Blog.objects.get(id=pk)
        if request.user.id == blog.owner_id:
            form = CreatePostForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                title = form.data.get('title')
                content = form.data.get('content')
                image = form.files.get('image', None)
                post = Post(title=title, content=content, blog_id=blog.id, image=image)
                post.save()
                return redirect('/blogs/' + str(blog.id) + '/')
            else:
                return render(request, 'blogs/blog-details.html', {'blog': blog, 'user': request.user, 'form': form})
        else:
            return redirect('/')


@user_passes_test(lambda u: u.is_staff)
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if post.blog.owner.id == request.user.id:
        post.delete()
        return redirect('/blogs/' + str(post.blog.id) + '/')
    else:
        return redirect('/')


def post_details(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'blogs/post-details.html', {'post': post})
