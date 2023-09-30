from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddTaskForm
from .models import Task


# Create your views here.
def home(request):
    # tasks = Record.objects.all()
    tasks = []
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in...")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging you in.. Please try again...")
            return redirect('home')

    else:
        return render(request, 'home.html', {"tasks": tasks})


def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully registered...")
            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, 'register.html', {"form": form})

    return render(request, 'register.html', {"form": form})


def get_task(request, pk):
    if request.user.is_authenticated:
        user_tasks = Task.objects.get(id=pk)

        return render(request, 'task.html', {"user_tasks": user_tasks})

    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect("home")


def delete_task(request, pk):
    if request.user.is_authenticated:
        current_task = Task.objects.get(id=pk)
        current_task.delete()
        messages.success(request, "Task deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete this task...")
        return redirect("home")


def add_task(request):
    form = AddTaskForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                # add_user_task = form.save()
                task = request.POST.get('task')
                description = request.POST.get('description')
                Task.objects.create(user=request.user, task=task, description=description)
                messages.success(request, "Task added successfully...")
                return redirect('home')

        else:
            return render(request, 'add_task.html', {'form': form})

    else:
        messages.success(request, "You must be logged in to add a record...")
        return redirect(home)


def update_task(request, pk):
    if request.user.is_authenticated:
        current_task = Task.objects.get(id=pk)
        form = AddTaskForm(request.POST or None, instance=current_task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully...")
            return redirect('home')
        return render(request, 'update_task.html', {'form': form})

    else:
        messages.success(request, "You must be logged in to update a task...")
        return redirect('home')
