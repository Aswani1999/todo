from django import forms
from .models import Project
from .models import Todo


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']

from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description', 'status']



from django import forms
from .models import Todo

class TodoForms(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['id', 'description']  # Adjust the fields as needed




# forms.py
from django import forms
from .models import Todo

class AddTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description']  # You can include more fields here if needed

    def __init__(self, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = project_id

    def save(self, commit=True):
        todo = super().save(commit=False)
        todo.project_id = self.project_id
        if commit:
            todo.save()
        return todo


