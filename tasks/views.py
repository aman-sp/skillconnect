from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Task, Application
from .forms import TaskForm, ApplicationForm


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/task_list.html", {
        "page_obj": page_obj
    })


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.posted_by = request.user
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("tasks")
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {"form": form})


@login_required
def apply_for_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.task = task
            application.freelancer = request.user
            application.save()
            messages.success(request, "Application submitted!")
            return redirect("task_detail", id=id)

    else:
        form = ApplicationForm()

    return render(request, "tasks/apply.html", {
        "task": task,
        "form": form
    })
