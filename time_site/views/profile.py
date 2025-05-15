from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from time_site.models import CustomUser, WorkLog
from time_site.forms import ProfileEditForm
from django.utils.timezone import now, timedelta


@login_required
def profile_view(request):
    profile_user = request.user  # Текущий авторизованный пользователь
    user_id = request.GET.get('user_id')  # Получаем user_id из URL, если это необходимо
    if user_id and (
            request.user.is_admin or request.user.is_staff):  # Если есть user_id и пользователь администратор или персонал
        profile_user = get_object_or_404(CustomUser, id=user_id)

    # Проверяем, является ли текущий пользователь владельцем профиля
    is_own_profile = profile_user == request.user

    context = {
        'user': request.user,
        'profile_user': profile_user,
        'department_display': profile_user.department.name if profile_user.department else 'Не указан',
        'role_display': profile_user.get_role_display(),
        'is_own_profile': is_own_profile  # Передаем переменную в контекст
    }

    return render(request, 'profile/view.html', context)


@login_required
def profile_edit(request):
    profile_user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # После сохранения редиректим на просмотр профиля
    else:
        form = ProfileEditForm(instance=profile_user)

    return render(request, 'profile/edit.html', {'form': form, 'profile_user': profile_user})

def public_profile_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    period = request.GET.get('period', '30')  # по умолчанию 30 дней
    try:
        days = int(period)
    except ValueError:
        days = 30

    start_date = now().date() - timedelta(days=days)
    logs = WorkLog.objects.filter(user=user, date__gte=start_date).order_by('-date')

    return render(request, 'profile/public_profile.html', {
        'user_profile': user,
        'logs': logs,
        'selected_period': days,
    })