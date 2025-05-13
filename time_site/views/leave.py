from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from time_site.forms import LeaveRequestForm
from time_site.models import LeaveRequest
from django.utils import translation
from django.http import HttpResponseForbidden
from time_site.models import CustomUser


translation.activate("ru")


@login_required
def leave_form_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/leave_form.html', {'form': form})


@login_required
def leave_list_view(request):
    leaves = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'leave/leave_list.html', {'leaves': leaves})


@login_required
def leave_edit_view(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, user=request.user)
    if leave.status != 'на рассмотрении':
        return redirect('leave_list')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveRequestForm(instance=leave)

    return render(request, 'leave/leave_form.html', {'form': form, 'edit': True})


@login_required
def leave_delete_view(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, user=request.user)
    if leave.status == 'на рассмотрении':
        leave.delete()
    return redirect('leave_list')


@login_required
def leave_approval_list_view(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("Доступ запрещён")

    # Получаем сотрудников из отдела руководителя
    employees = CustomUser.objects.filter(department=request.user.department)
    leaves = LeaveRequest.objects.filter(user__in=employees).order_by('-submitted_at')

    return render(request, 'leave/leave_approval_list.html', {'leaves': leaves})


@login_required
def approve_leave_view(request, pk):
    if not request.user.is_manager:
        return HttpResponseForbidden()

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.user.department != request.user.department:
        return HttpResponseForbidden("Можно управлять только заявками своего отдела")

    leave.status = 'одобрено'
    leave.save()
    return redirect('leave_approval_list')


@login_required
def reject_leave_view(request, pk):
    if not request.user.is_manager:
        return HttpResponseForbidden()

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.user.department != request.user.department:
        return HttpResponseForbidden("Можно управлять только заявками своего отдела")

    leave.status = 'отклонено'
    leave.save()
    return redirect('leave_approval_list')