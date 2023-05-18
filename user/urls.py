from django.urls import path
from user.views import login_page, register_page, logout_page, settings_page

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='registration'),
    path('logout/', logout_page, name='logout'),
    path('settings/', settings_page, name='settings_page')
]
