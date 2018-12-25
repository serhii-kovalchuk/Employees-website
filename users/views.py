from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrarionForm


def registration(request):

	if request.method == 'POST':
		form = UserRegistrarionForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('users-login')
	else:
		form = UserRegistrarionForm()

	return render(request, 'users/registration.html',
	 {'form': form})

