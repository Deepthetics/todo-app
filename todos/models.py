from django.db import models

class Todo(models.Model):
    """
    Represents a task to be completed.

    Fields:
    - description (CharField): A short description of the task (max 200 characters).
    - user (ForeignKey): The user who created the task (referenced by their ID).
    """
    
    description = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
