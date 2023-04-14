from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Todo

def todos(request):
    """
    Displays a list of all Todos.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """

    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todos/todos.html', context)

def add_todo(request):
    """
    Adds a new Todo to the database.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response redirecting to the list of Todos.
    """

    if request.method == 'POST':
        description = request.POST['description']
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            todo = Todo.objects.create(description=description, user=user)
            todo.save()
            return HttpResponseRedirect(reverse('todos'))
        except User.DoesNotExist:
            return redirect(reverse('todos') + '?error_message=User with username {} does not exist'.format(username))
    else:
        return HttpResponseNotAllowed(['POST'])

def delete_todo(request, todo_id):
    """
    Deletes a Todo from the database.

    Args:
        request (HttpRequest): The HTTP request.
        todo_id (int): The ID of the Todo to be deleted.

    Returns:
        HttpResponse: The HTTP response redirecting to the list of Todos.
    """

    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.delete()
        return HttpResponseRedirect(reverse('todos'))
    else:
        return HttpResponseNotAllowed(['POST'])

def update_todo(request, todo_id):
    """
    Updates the description of a Todo in the database.

    Args:
        request (HttpRequest): The HTTP request.
        todo_id (int): The ID of the Todo to be updated.

    Returns:
        HttpResponse: The HTTP response redirecting to the list of Todos.
    """

    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.description = request.POST['new_description']
        todo.save()
        return HttpResponseRedirect(reverse('todos'))
    else:
        return HttpResponseNotAllowed(['POST'])
