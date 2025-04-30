from django.urls import path
from .views import home
from time_site.views.auth import login_view, register_view, logout_action
from time_site.views.profile import profile_view, profile_edit

urlpatterns = [
    path('', home, name='home'),  # Главная страница


    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_action, name='logout'),


    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]