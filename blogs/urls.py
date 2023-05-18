from django.urls import path
from blogs.views import home_page, create_blog_page, blog_details_page, delete_blog_page, create_blogs_post, \
    delete_post, post_details, blog_details_page_for_staff

urlpatterns = [
    path('', home_page, name='home_page'),
    path('blogs/create/', create_blog_page, name='create_blog_page'),
    path('blogs/<int:pk>/', blog_details_page, name='blog_details_page'),
    path('blogs/<int:pk>/', blog_details_page_for_staff, name='blog_details_page'),
    path('blogs/<int:pk>/delete/', delete_blog_page, name='delete_blog_page'),
    path('blogs/<int:pk>/posts-create/', create_blogs_post, name='create_blogs_post'),
    path('posts/<int:pk>/delete/', delete_post, name='delete_post'),
    path('posts/<int:pk>/', post_details, name='post_details'),
]

