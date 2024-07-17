# Tasks/forms.py

from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']




class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Users', max_length=100)



from .models import Task
from Users.models import CustomUser  # Adjust the import based on your actual app structure

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to', 'project', 'completed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = CustomUser.objects.all()
