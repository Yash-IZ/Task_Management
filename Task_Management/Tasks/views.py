from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task
from .forms import ProjectForm, UserSearchForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Users.models import CustomUser as User

@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.manager = request.user
            project.save()
            return redirect('add_members', pk=project.pk)
    else:
        project_form = ProjectForm()
    
    return render(request, 'Tasks/create_project.html', {
        'project_form': project_form,
    })

@login_required
def add_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user_search_form = UserSearchForm(request.GET or None)
    users = User.objects.none()

    if user_search_form.is_valid():
        search_query = user_search_form.cleaned_data['search_query']
        users = User.objects.filter(username__icontains=search_query)
    
    if request.method == 'POST' and 'add_member' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        project.members.add(user)
        project.save()
        return redirect('add_members', pk=project.pk)

    if request.method == 'POST' and 'confirm_members' in request.POST:
        # Handle confirmation logic here, e.g., redirect to project detail page
        return redirect('project_detail', pk=project.pk)

    return render(request, 'Tasks/add_members.html', {
        'project': project,
        'user_search_form': user_search_form,
        'users': users,
    })

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # You can include task related logic here if needed
    return render(request, 'Tasks/project_detail.html', {'project': project})

def task_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'Tasks/task_list.html', {'project': project, 'tasks': tasks})


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Check if the current user is the manager of the project
    if request.user != project.manager:
        messages.error(request, 'You are not authorized to create tasks for this project.')
        return redirect('project_detail', pk=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project_id = project_id  # Set the project for the task
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm()
    
    return render(request, 'Tasks/create_task.html', {'form': form})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'Tasks/task_detail.html', {'task': task})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project

    # Check if the current user is the manager of the project
    if request.user != project.manager:
        messages.error(request, 'You are not authorized to update tasks for this project.')
        return redirect('task_detail', task_id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', task_id=task_id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'Tasks/update_task.html', {'form': form, 'task': task})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project

    # Check if the current user is the manager of the project or the assigned user
    if request.user != project.manager and request.user != task.assigned_to:
        messages.error(request, 'You are not authorized to complete this task.')
        return redirect('task_detail', task_id=task_id)

    task.completed = True
    task.save()
    messages.success(request, 'Task marked as complete.')
    return redirect('task_detail', task_id=task_id)
