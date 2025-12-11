from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Task, Application
from .forms import TaskForm, ApplicationForm


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')

    paginator = Paginator(tasks, 5)  # Show 5 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/task_list.html", {
        "page_obj": page_obj
    })


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    applications = Application.objects.filter(task=task)

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "applications": applications
    })


@login_required
def create_task(request):
    if request.user.userprofile.role != "poster":
        messages.error(request, "Only task posters can create tasks.")
        return redirect("/tasks/")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.posted_by = request.user
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("/tasks/")
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {
        "form": form
    })


@login_required
def apply_to_task(request, id):
    task = get_object_or_404(Task, id=id)

    # Block posters from applying to their own task
    if task.posted_by == request.user:
        messages.error(request, "You cannot apply to your own task.")
        return redirect(f"/tasks/{id}/")

    # Prevent duplicate application
    if Application.objects.filter(task=task, freelancer=request.user).exists():
        messages.error(request, "You have already applied to this task.")
        return redirect(f"/tasks/{id}/")

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.task = task
            app.freelancer = request.user
            app.save()
            messages.success(request, "Application submitted successfully!")
            return redirect(f"/tasks/{id}/")
    else:
        form = ApplicationForm()

    return render(request, "tasks/apply.html", {
        "task": task,
        "form": form
    })
