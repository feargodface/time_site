from django.urls import path
from .views import home
from time_site.views.auth import login_view, register_view, logout_action
from .views import departments as department_views
from time_site.views.profile import profile_view, profile_edit, public_profile_view


urlpatterns = [
    path('', home, name='home'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_action, name='logout'),


    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/<int:user_id>/', public_profile_view, name='public_profile'),

    path('departments/', department_views.department_list, name='department_list'),
    path('departments/<int:pk>/', department_views.department_detail, name='department_detail'),
]