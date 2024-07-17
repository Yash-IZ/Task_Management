from django.shortcuts import render
from Tasks.models import Project

def home(request):
    if request.user.is_authenticated:
        # Fetch projects where the user is either a manager or a member
        managed_projects = Project.objects.filter(manager=request.user)
        member_projects = Project.objects.filter(members=request.user)
        projects = managed_projects | member_projects
        projects = projects.distinct()  # Ensure there are no duplicates
        context = {'projects': projects}
    else:
        context = {}
    return render(request, 'main_app/home.html', context)
