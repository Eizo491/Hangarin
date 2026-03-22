import os
import django
import random
from faker import Faker
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin_config.settings')
django.setup()

from tasks.models import Task, Category, Priority, Note, SubTask

fake = Faker()

def populate(n=10):
    # Get existing categories and priorities (ensure you added them via Admin first!)
    categories = list(Category.objects.all())
    priorities = list(Priority.objects.all())

    if not categories or not priorities:
        print("Please add Categories and Priorities via Admin before running this script.")
        return

    for _ in range(n):
        # 1. Create Task [cite: 96-98]
        # Requirement: Use sentence(nb_words=5) and paragraph(nb_sentences=3) [cite: 99-101]
        # Requirement: Use timezone.make_aware() [cite: 42-44]
        deadline = timezone.make_aware(fake.date_time_this_month()) 
        
        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=deadline,
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
            category=random.choice(categories),
            priority=random.choice(priorities)
        )

        # 2. Create Notes for the task [cite: 83]
        for _ in range(random.randint(1, 3)):
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        # 3. Create SubTasks for the task [cite: 83]
        for _ in range(random.randint(2, 4)):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

    print(f"Successfully populated {n} tasks with notes and subtasks!")

if __name__ == '__main__':
    populate(15)