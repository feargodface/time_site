from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Department, CustomUser
from django.shortcuts import get_object_or_404

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    employees = department.employees.all()
    managers = employees.filter(role='Руководитель')
    return render(request, 'departments/detail.html', {
        'department': department,
        'managers': managers,
        'employees': employees,
    })

