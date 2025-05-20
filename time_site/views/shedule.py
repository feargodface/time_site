from django.shortcuts import render
from time_site.models import DepartmentWorkSchedule

WEEKDAYS = [
    (0, "Понедельник"),
    (1, "Вторник"),
    (2, "Среда"),
    (3, "Четверг"),
    (4, "Пятница"),
    (5, "Суббота"),
    (6, "Воскресенье"),
]

def work_schedules_view(request):
    schedules = DepartmentWorkSchedule.objects.select_related("department").all()
    schedules_with_days = []

    for schedule in schedules:
        working_days = [int(d) for d in schedule.working_days.split(",")]
        schedules_with_days.append({
            "department": schedule.department.name,
            "work_start": schedule.work_start,
            "work_end": schedule.work_end,
            "working_days": working_days
        })

    context = {
        "schedules": schedules_with_days,
        "weekdays": WEEKDAYS,
    }
    return render(request, "shedule/work_shedules.html", context)
