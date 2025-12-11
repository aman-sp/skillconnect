from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import SignupForm, UserProfileForm

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
        profile_form = UserProfileForm()

    return render(request, "accounts/signup.html", {
        "form": form,
        "profile_form": profile_form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")
