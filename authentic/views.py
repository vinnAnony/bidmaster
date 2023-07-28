from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


User = get_user_model()


def sign_up(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("authentic:log_in"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            
            return redirect(reverse("authentic:sign_up"))

    return render(request, "authentic/signup.html", {"form": form})


def log_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse("bidding:index"))
        else:
            print(form.errors)
    return render(request, "authentic/login.html", {"form": form})


@login_required
def log_out(request):
    logout(request)
    return redirect(reverse("authentic:log_in"))
