from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from time_site.forms import ProfileEditForm
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'accounts/profile/view.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile_view')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/profile/edit.html', {'form': form})