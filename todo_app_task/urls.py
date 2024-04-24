# from django.urls import path
# from .views import Index

# urlpatterns = [
#     path('',Index.as_view(),name='index'),
 
# ]



# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views


# urlpatterns = [
#     path('', views.index, name='index'),
#     path('login/', views.login, name='login'),
#     # path('logout/', views.logout, name='logout'),
# ]


from django.urls import path 
from . import views
from django.urls import reverse
from .views import *

from .views import create_project,project_list,project_lists,add_todo
from .views import update_todo_status,export_summary,delete_todo,project_detail,update_todo_description


urlpatterns = [
    # path('', views.dashboard_view, name='dashboard'), 
    # path('register/',views.register_view,name='register'),
    # path('login/',views.login_view,name='login'),
    # path('logout/',views.logout_view,name='logout'),
    
    # path('dashboard/',views.dashboard_view,name='dashboard')

    path('',views.HomePage,name='home'),
    path('signups/',views.SignupPage,name='signups'),
    path('login/',views.LoginPage,name='login'),
    path('project_list/', views.project_list, name='project_list'),
    path('project_lists/', views.project_lists, name='project_lists'),
    path('create_project/', create_project, name='create_project'),
    path('add_todo/', add_todo, name='add_todo'),
     # URL pattern for updating todo status
    path('update_todo_status/<int:todo_id>/', update_todo_status, name='update_todo_status'),

    # URL pattern for deleting todo
    path('delete_todo/<int:todo_id>/', delete_todo, name='delete_todo'),
    path('project_detail/<int:project_id>/', project_detail, name='project_detail'),

    # URL pattern for exporting summary
    path('export_summary/', export_summary, name='export_summary'),
    path('update_todo_description/', update_todo_description, name='update_todo_description'),
    path('update_todo_description/<int:todo_id>/', update_todo_description, name='update_todo_description'),
    # path('project/<int:project_id>/', project_detail_view, name='project_detail'),
    # path('new/',views.new,name='new'),
    # path('logout/',views.LogoutPage,name='logout'),

]