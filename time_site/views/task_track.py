from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from time_site.models import TeamTask
from time_site.forms import TeamTaskForm
from django.http import HttpResponseForbidden



def task_list(request):
    user = request.user
    tasks = TeamTask.objects.all()

    if user.department:
        tasks = tasks.filter(department=user.department)

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    return render(request, 'task_track/task_list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TeamTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.department = request.user.department
            task.status = 'свободна'
            task.save()
            return redirect('task_list')
    else:
        form = TeamTaskForm()
    return render(request, 'task_track/create_task.html', {'form': form})


@login_required
def take_task(request, task_id):
    task = get_object_or_404(TeamTask, id=task_id, status='свободна', assigned_to__isnull=True)
    task.assigned_to = request.user
    task.status = 'в работе'
    task.save()
    messages.success(request, "Вы взяли задачу в работу.")
    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(TeamTask, id=task_id, assigned_to=request.user, status='в работе')
    task.status = 'завершена'
    task.save()
    messages.success(request, "Вы отметили задачу как завершенную.")
    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(TeamTask, id=task_id)

    if not request.user.is_manager or task.assigned_to:
        return HttpResponseForbidden("Редактирование запрещено.")

    if request.method == 'POST':
        form = TeamTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TeamTaskForm(instance=task)

    return render(request, 'task_track/edit_task.html', {'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(TeamTask, id=task_id)

    if not request.user.is_manager or task.assigned_to:
        return HttpResponseForbidden("Удаление запрещено.")

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')