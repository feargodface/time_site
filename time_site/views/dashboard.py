from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta, datetime
from time_site.models import WorkLog, LeaveRequest

@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()
    start_of_month = today.replace(day=1)

    # Получаем WorkLog за период
    work_logs_qs = WorkLog.objects.filter(
        user=user,
        date__gte=start_of_month,
        date__lte=today
    ).order_by('date')

    # Считаем минуты вручную
    work_log_dict = {}
    for log in work_logs_qs:
        if log.check_in and log.check_out:
            dt_check_in = datetime.combine(log.date, log.check_in)
            dt_check_out = datetime.combine(log.date, log.check_out)
            worked_minutes = (dt_check_out - dt_check_in).total_seconds() / 60 - log.break_minutes
            worked_minutes = max(worked_minutes, 0)
        else:
            worked_minutes = 0
        work_log_dict[log.date] = work_log_dict.get(log.date, 0) + worked_minutes

    dates = []
    hours = []
    current_day = start_of_month

    while current_day <= today:
        dates.append(current_day.strftime('%Y-%m-%d'))
        minutes = work_log_dict.get(current_day, 0)
        hours.append(round(minutes / 60, 2))
        current_day += timedelta(days=1)

    # Подсчёт дней отпуска
    leaves = LeaveRequest.objects.filter(
        user=user,
        status='одобрено',
        start_date__year=today.year
    )

    used_leave_days = 0
    for leave in leaves:
        delta = (leave.end_date - leave.start_date).days + 1
        used_leave_days += delta

    total_leave_days = 28
    remaining_leave_days = max(total_leave_days - used_leave_days, 0)

    context = {
        'dates': dates,
        'hours': hours,
        'used_leave_days': used_leave_days,
        'remaining_leave_days': remaining_leave_days,
        'total_leave_days': total_leave_days,
    }
    return render(request, 'time_site/dashboard.html', context)
