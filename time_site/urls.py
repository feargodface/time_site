from django.urls import path
from .views import home
from time_site.views.auth import login_view, register_view, logout_action
from .views import departments as department_views
from time_site.views.profile import profile_view, profile_edit, public_profile_view
from time_site.views.statistics import my_statistics_view, department_statistics_view, export_department_excel
from time_site.views.leave import (
    leave_form_view, leave_list_view, leave_edit_view, leave_delete_view,
    leave_approval_list_view, approve_leave_view, reject_leave_view, export_department_leaves_excel
)



urlpatterns = [
    path('', home, name='home'),

#---авторизация/регистрация
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_action, name='logout'),

#----профили
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/<int:user_id>/', public_profile_view, name='public_profile'),

#----отделы
    path('departments/', department_views.department_list, name='department_list'),
    path('departments/<int:pk>/', department_views.department_detail, name='department_detail'),

#----все про статистику
    path('statistics/', my_statistics_view, name='my_statistics'),
    path('departments/<int:pk>/statistics/', department_statistics_view, name='department_statistics'),
    path('departments/<int:pk>/statistics/export/', export_department_excel, name='export_department_excel'),

#---заявки
    path('leave/request/', leave_form_view, name='leave_form'),
    path('leave/my/', leave_list_view, name='leave_list'),
    path('leave/<int:pk>/edit/', leave_edit_view, name='leave_edit'),
    path('leave/<int:pk>/delete/', leave_delete_view, name='leave_delete'),
    path('leaves/department/export/', export_department_leaves_excel, name='export_department_leaves_excel'),

    #---ЗАЯВКИ для руководителя
    path('leave/approval/', leave_approval_list_view, name='leave_approval_list'),
    path('leave/<int:pk>/approve/', approve_leave_view, name='leave_approve'),
    path('leave/<int:pk>/reject/', reject_leave_view, name='leave_reject'),

]