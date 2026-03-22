from django.test import TestCase
from .models import Task, Category, Priority, SubTask
from django.utils import timezone

class BaseModelTest(TestCase):
    def setUp(self):
        # Setup basic requirements for a task
        self.category = Category.objects.create(name="School")
        self.priority = Priority.objects.create(name="High")

    def test_inheritance_timestamps(self):
        # Create a Task
        task = Task.objects.create(
            title="Finish PSU Lab",
            description="Complete the Midterm requirements",
            deadline=timezone.now(),
            category=self.category,
            priority=self.priority
        )
        
        # Create a SubTask
        subtask = SubTask.objects.create(
            title="Refactor Models",
            parent_task=task
        )

        # Assertions: Check if timestamps exist (inheritance check)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(subtask.created_at)
        
        # Verify specific SubTask requirement
        self.assertEqual(subtask.parent_task.title, "Finish PSU Lab")

        print("\n BaseModel Inheritance Test: PASSED")
        print("SubTask Relationship Test: PASSED")