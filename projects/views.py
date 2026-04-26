from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Project, Task


@login_required
def dashboard(request):
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    my_tasks = Task.objects.filter(assigned_to=request.user).exclude(status='done').order_by('due_date')
    total_projects = projects.count()
    active_projects = projects.filter(status='active').count()
    completed_projects = projects.filter(status='completed').count()
    total_tasks = Task.objects.filter(project__created_by=request.user).count()
    context = {
        'projects': projects[:5],
        'my_tasks': my_tasks[:5],
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_tasks': total_tasks,
    }
    return render(request, 'projects/dashboard.html', context)


@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    tasks = project.tasks.all().order_by('status', 'due_date')
    users = User.objects.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks, 'users': users})


@login_required
def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline') or None
        Project.objects.create(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            created_by=request.user,
        )
        messages.success(request, 'Project created successfully!')
        return redirect('project_list')
    return render(request, 'projects/project_form.html', {'action': 'Create'})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.status = request.POST.get('status')
        project.deadline = request.POST.get('deadline') or None
        project.save()
        messages.success(request, 'Project updated successfully!')
        return redirect('project_detail', pk=pk)
    return render(request, 'projects/project_form.html', {'action': 'Edit', 'project': project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, created_by=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date') or None
        assigned_to_id = request.POST.get('assigned_to') or None
        assigned_to = User.objects.filter(pk=assigned_to_id).first() if assigned_to_id else None
        Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,
        )
        messages.success(request, 'Task added!')
        return redirect('project_detail', pk=project_pk)
    users = User.objects.all()
    return render(request, 'projects/task_form.html', {'project': project, 'users': users, 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date') or None
        assigned_to_id = request.POST.get('assigned_to') or None
        task.assigned_to = User.objects.filter(pk=assigned_to_id).first() if assigned_to_id else None
        task.save()
        messages.success(request, 'Task updated!')
        return redirect('project_detail', pk=project.pk)
    users = User.objects.all()
    return render(request, 'projects/task_form.html', {'task': task, 'project': project, 'users': users, 'action': 'Edit'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
    return redirect('project_detail', pk=project_pk)
