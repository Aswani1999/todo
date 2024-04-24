from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')


def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signups.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')





from .models import Project, Todo  

def project_list(request):

    projects = Project.objects.all()

    project_todos = {}
    for project in projects:
        todos = Todo.objects.filter(project=project)
        project_todos[project] = todos

    return render(request, 'project_list.html', {'project_todos': project_todos})

    # def new(request):
    #     return render(request,'project_list.html')
from django.shortcuts import render, redirect
from .models import Project

def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        project = Project(title=title)
        project.save()
        return redirect('project_list') 
    return render(request, 'create_project.html')









# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Project, Todo
import requests

from django.http import JsonResponse, HttpResponseNotAllowed
from django.http import JsonResponse
import json

def update_todo_status(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        if status in ['complete', 'pending']:  # Ensure status is one of the allowed values
            todo.status = status
            todo.save()
            return JsonResponse({'message': 'Todo status updated successfully.'})
        else:
            return JsonResponse({'error': 'Invalid status value.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def delete_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.delete()
        return JsonResponse({'message': 'Todo deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
from django.shortcuts import render
from django.http import JsonResponse
from .models import Project, Todo
import requests
import json
import os
from django.conf import settings

from django.http import JsonResponse
from django.http import JsonResponse
from .models import Project, Todo
import requests
import json
import os
from django.conf import settings

import traceback  # Import traceback module for error logging

def export_summary(request):
    if request.method == 'POST':
        try:
           
            project = Project.objects.first()
            
            # Fetch todos associated with the project
            todos = Todo.objects.filter(project=project)
            
            # Extract pending and completed todos
            pending_todos = []
            completed_todos = []
            for todo in todos:
                if todo.status == 'pending':
                    pending_todos.append(todo.description)
                elif todo.status == 'complete':
                    completed_todos.append(todo.description)
            
            # Export summary to Gist
            gist_url = export_project_summary_to_gist(project.title, pending_todos, completed_todos)
            if gist_url:
                # Save exported gist file to local system as markdown
                save_gist_as_markdown(project.title, gist_url)
                return JsonResponse({'gist_url': gist_url})
            else:
                return JsonResponse({'error': 'Failed to create gist'}, status=500)
        except Exception as e:
            # Log the exception for debugging
            traceback.print_exc()  # Print traceback to console
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# def export_summary(request):
#     if request.method == 'POST':
#         try:
#             # Fetch the first project
#             project = Project.objects.first()
            
#             # Fetch todos associated with the project
#             todos = Todo.objects.filter(project=project)
            
#             # Extract pending and completed todos
#             pending_todos = []
#             completed_todos = []
#             for todo in todos:
#                 if todo.status == 'pending':
#                     pending_todos.append(todo.description)
#                 elif todo.status == 'complete':
#                     completed_todos.append(todo.description)
            
#             # Export summary to Gist
#             gist_url = export_project_summary_to_gist(project.title, pending_todos, completed_todos)
            
#             if gist_url:
#                 # Save exported gist file to local system as markdown
#                 save_gist_as_markdown(project.title, gist_url)
#                 return JsonResponse({'gist_url': gist_url})
#             else:
#                 return JsonResponse({'error': 'Failed to create gist'}, status=500)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

def export_project_summary_to_gist(project_title, pending_todos, completed_todos):
    # Calculate total todos and completed todos
    total_todos = len(pending_todos) + len(completed_todos)
    completed_count = len(completed_todos)
    
    # Generate markdown content
    markdown_content = f"# {project_title}\n\n"
    markdown_content += f"**Summary:** {completed_count} / {total_todos} completed.\n\n"
    
    # Section 1: Pending todos
    markdown_content += "## Pending Todos\n\n"
    markdown_content += generate_task_list(pending_todos, False) + "\n\n"
    
    # Section 2: Completed todos
    markdown_content += "## Completed Todos\n\n"
    markdown_content += generate_task_list(completed_todos, True)
    
    # Prepare payload for creating the gist
    payload = {
        'files': {
            f'{project_title}.md': {
                'content': markdown_content
            }
        },
        'public': False,
        'description': 'Project Summary'
    }
    load_dotenv()

    github_access_token = os.environ.get('GITHUB_ACCCESS_TOKEN')
    print(github_access_token)
    # Define the headers with the Authorization token
    headers = {
    'Authorization': f'token {github_access_token}'
    }

    # Create the gist
    response = requests.post('https://api.github.com/gists', data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        gist_data = response.json()
        gist_url = gist_data['html_url']
        print(f"Gist created successfully. URL: {gist_url}")
        return gist_url  # Return the URL of the created gist
    else:
        print("Failed to create gist.")
        return None

def generate_task_list(tasks, checked):
    task_list = ""
    for task in tasks:
        task_list += f"- [{'x' if checked else ' '}] {task}\n"
    return task_list

import os
from pathlib import Path

import os
import requests
from pathlib import Path

def save_gist_as_markdown(file_name, gist_url):
    print(file_name, gist_url)
    # Fetch the content of the gist
    response = requests.get(gist_url)

    try:
        if response.status_code == 200:
            gist_content = response.text
            # print("Gist data:", gist_data)  # Add this line for debugging
            # gist_content = gist_data['files'][file_name]['content']
            directory_path = './exported_gists'

            # Create the directory if it doesn't exist
            Path(directory_path).mkdir(parents=True, exist_ok=True)

            # Define the path to save the markdown file
            save_path = os.path.join(directory_path, f'{file_name}.md')

            # Save the gist content as markdown
            with open(save_path, 'w') as file:
                file.write(gist_content)

            print(f"Gist content saved as Markdown: {save_path}")
        else:
            print("Failed to fetch gist content.")
    except Exception as e:
        print("Failed to parse gist content:", e)
        # print("Response text:", response.text)

# def save_gist_as_markdown(project_title, gist_url):
#     # Define the directory path where you want to save the files
#     directory_path = os.path.join(settings.BASE_DIR, 'exported_gists')
#     print(directory_path)
#     # Create the directory if it doesn't exist
#     if not os.path.exists(directory_path):
#         try:
#             os.makedirs(directory_path)
#         except OSError as e:
#             print(f"Failed to create directory: {directory_path}")
#             print(e)
#             return
    
#     # Fetch the content of the gist
#     response = requests.get(gist_url)
#     if response.status_code == 200:
#         gist_content = response.json()['files'][f'{project_title}.md']['content']
        
#         # Define the path to save the markdown file
#         save_path = os.path.join(directory_path, f'{project_title}.md')
        
#         # Save the gist content as markdown
#         try:
#             with open(save_path, 'w') as file:
#                 file.write(gist_content)
#             print(f"Gist content saved as markdown: {save_path}")
#         except OSError as e:
#             print(f"Failed to save gist content as markdown: {save_path}")
#             print(e)
#     else:
#         print("Failed to fetch gist content.")



from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Todo
from .forms import TodoForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Project, Todo
from .forms import TodoForm

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    todos = Todo.objects.filter(project=project)

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.instance.project = project
            form.save()
            return redirect('project_detail', project_id=project_id)
        else:
            # If the form is not valid, handle the update title form
            title = request.POST.get('title')
            if title:
                project.title = title
                project.save()
                return redirect('project_detail', project_id=project_id)
    else:
        form = TodoForm()

    context = {
        'project': project,
        'todos': todos,
        'form': form,
        'project_id': project_id,  # Pass project_id to the template context
    }

    return render(request, 'project_detail.html', context)


# from django.shortcuts import render, get_object_or_404
# from .models import Project

# def project_list_view(request):
#     projects = Project.objects.all()
#     return render(request, 'projects.html', {'projects': projects})

# def project_detail_view(request, project_id):
#     project = get_object_or_404(Project, pk=project_id)
#     return render(request, 'project_detail.html', {'project': project})

from django.shortcuts import render, redirect
from .models import Todo
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Todo
from .forms import TodoForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TodoForm
from .models import Project, Todo
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Todo
from .forms import TodoForm

# views.py
from django.shortcuts import redirect, render
from .forms import AddTodoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import TodoForms,TodoForms,ProjectForm
from .models import Todo, Project
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # Disable CSRF protection for this view
def add_todo(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON data from request body
        project_id = data.get('project_id')
        description = data.get('description')
        
        if project_id is None or description is None:
            return JsonResponse({'error': 'Project ID or description is missing.'}, status=400)
        
        project = Project.objects.filter(pk=project_id).first()
        if project is None:
            return JsonResponse({'error': 'Project not found.'}, status=404)
        
        todo = Todo.objects.create(project=project, description=description)
        return JsonResponse({'message': 'Todo added successfully.'})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


# def add_todo(request):
#     if request.method == 'POST':
#         form = TodoForm(request.POST)
#         if form.is_valid():
#             project_id = request.POST.get('project_id')  # Get the project_id from the form data
#             project = get_object_or_404(Project, pk=project_id)
#             todo = form.save(commit=False)
#             todo.project = project
#             todo.save()
#             return redirect('project_detail', project_id=project_id)
#     else:
#         form = TodoForm()

#     return render(request, 'project_detail.html', {'form': form})

# def add_todo(request):
#     if request.method == 'POST':
#         project_id = request.POST.get('project_id')  # Get the project_id from the form
#         print(project_id)
#         if project_id:
#             project = get_object_or_404(Project, pk=project_id)
#             form = TodoForm(request.POST)
#             if form.is_valid():
#                 # Create a new Todo object and associate it with the project
#                 todo = form.save(commit=False)
#                 todo.project = project
#                 todo.save()
#                 return redirect('project_detail', project_id=project_id)
#     # If the request method is not POST or if the project_id is missing, render the same page again
#     return render(request, 'project_detail.html')


from django.shortcuts import render, get_object_or_404
from .models import Project

# def project_list_view(request):
#     projects = Project.objects.all()
#     return render(request, 'project_list.html', {'projects': projects})

def project_detail_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_detail.html', {'project': project})



from django.shortcuts import render
from .models import Project

def project_lists(request):
    # Retrieve all projects from the database
    projects = Project.objects.all()
    
    return render(request, 'project_lists.html', {'projects': projects})



# from .models import Todo
# @csrf_exempt  # Disable CSRF protection for this view
# def update_todo_description(request, todo_id):
#     if request.method == 'POST':
#         todo = Todo.objects.get(pk=todo_id)
#         new_description = request.POST.get('description')

#         # Update the todo description
#         todo.description = new_description
#         todo.save()

#         return JsonResponse({'message': 'Todo description updated successfully.'})
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Todo
import json

def update_todo_description(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_id)
        data = json.loads(request.body)
        new_description = data.get('description')
        if new_description:
            todo.description = new_description
            todo.save()
            return JsonResponse({'message': 'Todo description updated successfully.'})
        else:
            return JsonResponse({'error': 'New description cannot be empty.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# def update_todo_description(request, todo_id):
#     if request.method == 'POST':
#         data = json.loads(request.body)  # Parse JSON data from request body
#         new_description = data.get('description')
        
#         if new_description is None:
#             return JsonResponse({'error': 'New description is missing.'}, status=400)
        
#         todo = get_object_or_404(Todo, pk=todo_id)
#         todo.description = new_description
#         todo.save()
#         return JsonResponse({'message': 'Todo description updated successfully.'})
    
#     return JsonResponse({'error': 'Invalid request method.'}, status=405)
