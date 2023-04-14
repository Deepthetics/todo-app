"""This module contains URL patterns for the todos app.

The urlpatterns list maps URL patterns to their corresponding views. The patterns
determine which view function should handle an incoming request based on the URL
requested by the user.

The available URL patterns are:
- '' (empty path): displays a list of all the Todos
- 'add/': adds a new Todo to the list
- 'delete/<int:todo_id>/': deletes the Todo with the given ID
- 'update/<int:todo_id>/': updates the description of the Todo with the given ID
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos, name='todos'),
    path ('add/', views.add_todo, name='add_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('update/<int:todo_id>/', views.update_todo, name='update_todo'),
]
