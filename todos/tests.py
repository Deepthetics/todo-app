from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import Todo

class TodosViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.todo1 = Todo.objects.create(description='Test todo 1', user=self.user)
        self.todo2 = Todo.objects.create(description='Test todo 2', user=self.user)
    
    def test_todos_view_when_todos(self):
        """
        Tests that the todos view returns a 200 status code and the correct todos.
        """

        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo1.description)
        self.assertContains(response, self.todo2.description)

    def test_todos_view_when_no_todos(self):
        """
        Tests that the todos view returns a 200 status code and the correct message when there are no todos.
        """

        Todo.objects.all().delete()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No todos available')

    def test_add_todo_view_when_valid(self):
        """
        Tests that the add_todo view returns a 302 status code and adds the todo to the database when the request is valid.
        """

        response = self.client.post(reverse('add_todo'), {'description': 'Test todo 3', 'username': self.user.username})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 3)
        redirected_response = self.client.get(response.url)
        self.assertContains(redirected_response, 'Test todo 3')
    
    def test_add_todo_view_when_invalid_user(self):
        """
        Tests that the add_todo view returns a 302 status code and does not add the todo to the database when the request is invalid.
        """

        response = self.client.post(reverse('add_todo'), { 'description': 'Test todo 3', 'username': 'invaliduser' })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)
        redirected_response = self.client.get(response.url)
        self.assertContains(redirected_response, 'User with username invaliduser does not exist')
    
    def test_add_todo_view_when_invalid_method(self):
        """
        Tests that the add_todo view returns a 405 status code and does not add the todo to the database when the request method is invalid.
        """

        response = self.client.get(reverse('add_todo'), { 'description': 'Test todo 3', 'username': self.user.username })
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Todo.objects.count(), 2)
        todos_page = self.client.get(reverse('todos'))
        self.assertNotContains(todos_page, 'Test todo 3')

    def test_delete_todo_view_when_valid_id(self):
        """
        Tests that the delete_todo view returns a 302 status code and deletes the todo from the database when the given username is invalid.
        """

        response = self.client.post(reverse('delete_todo', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)
        redirected_response = self.client.get(response.url)
        self.assertNotContains(redirected_response, self.todo1.description)
        self.assertContains(redirected_response, self.todo2.description)
    
    def test_delete_todo_view_when_invalid_id(self):
        """
        Tests that the delete_todo view returns a 404 status code and does not delete the todo from the database when the given todo id is invalid.
        """

        response = self.client.post(reverse('delete_todo', args=[3]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Todo.objects.count(), 2)
        todos_page = self.client.get(reverse('todos'))
        self.assertContains(todos_page, self.todo1.description)
        self.assertContains(todos_page, self.todo2.description)

    def test_delete_todo_view_when_invalid_method(self):
        """
        Tests that the delete_todo view returns a 405 status code and does not delete the todo from the database when the request method is invalid.
        """

        response = self.client.get(reverse('delete_todo', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Todo.objects.count(), 2)
        todos_page = self.client.get(reverse('todos'))
        self.assertContains(todos_page, self.todo1.description)
        self.assertContains(todos_page, self.todo2.description)
    
    def test_update_todo_view_when_valid(self):
        """
        Tests that the update_todo view returns a 302 status code and updates the todo in the database when the request is valid.
        """

        response = self.client.post(reverse('update_todo', args=[self.todo1.id]), { 'new_description': 'Updated todo 1' })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(id=self.todo1.id).description, 'Updated todo 1')
        redirected_response = self.client.get(response.url)
        self.assertContains(redirected_response, 'Updated todo 1')
        self.assertContains(redirected_response, self.todo2.description)

    def test_update_todo_view_when_invalid_id(self):
        """
        Tests that the update_todo view returns a 404 status code and does not update the todo in the database when the given todo id is invalid.
        """

        response = self.client.post(reverse('update_todo', args=[3]), { 'new_description': 'Updated todo 3' })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Todo.objects.count(), 2)
        todos_page = self.client.get(reverse('todos'))
        self.assertContains(todos_page, self.todo1.description)
        self.assertContains(todos_page, self.todo2.description)
    
    def test_update_todo_view_when_invalid_method(self):
        """
        Tests that the update_todo view returns a 405 status code and does not update the todo in the database when the request method is invalid.
        """

        response = self.client.get(reverse('update_todo', args=[self.todo1.id]), { 'new_description': 'Updated todo 1' })
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Todo.objects.count(), 2)
        todos_page = self.client.get(reverse('todos'))
        self.assertContains(todos_page, self.todo1.description)
        self.assertContains(todos_page, self.todo2.description)
