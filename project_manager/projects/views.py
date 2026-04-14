from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/dashboard.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})