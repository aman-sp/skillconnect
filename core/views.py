from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Application


def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    profile = request.user.userprofile

    # Poster Dashboard
    if profile.role == "poster":
        tasks = Task.objects.filter(posted_by=request.user)
        task_data = []
        for t in tasks:
            apps = Application.objects.filter(task=t)
            task_data.append({
                "task": t,
                "applications": apps.count()
            })

        return render(request, "core/dashboard_poster.html", {
            "task_data": task_data
        })

    # Freelancer Dashboard
    if profile.role == "freelancer":
        applications = Application.objects.filter(freelancer=request.user)

        return render(request, "core/dashboard_freelancer.html", {
            "applications": applications
        })
