from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from time_site.models import WorkLog
from time_site.forms import WorkLogForm
from django.utils.timezone import now

@login_required
def my_statistics_view(request):
    today = now().date()
    logs = WorkLog.objects.filter(user=request.user).order_by('-date')[:30]
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            log, created = WorkLog.objects.get_or_create(user=request.user, date=today)
            for field in form.cleaned_data:
                setattr(log, field, form.cleaned_data[field])
            log.save()
            return redirect('my_statistics')
    else:
        form = WorkLogForm()

    return render(request, 'statistics/my_stats.html', {
        'form': form,
        'logs': logs,
        'today': today,
    })