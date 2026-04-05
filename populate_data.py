import os
import django
import random
from faker import Faker
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin_config.settings')
django.setup()

# Added User to the imports
from django.contrib.auth.models import User
from tasks.models import Task, Category, Priority, Note, SubTask

fake = Faker()

def populate(n=10):
    # 1. Get a user to own these tasks (Crucial for fixing the IntegrityError)
    user = User.objects.first()
    
    # 2. Get existing categories and priorities
    categories = list(Category.objects.all())
    priorities = list(Priority.objects.all())

    if not user:
        print("Error: No users found. Run 'python manage.py createsuperuser' first.")
        return

    if not categories or not priorities:
        print("Please add Categories and Priorities via Admin before running this script.")
        return

    for _ in range(n):
        deadline = timezone.make_aware(fake.date_time_this_month()) 
        
        # 3. Create Task with the 'user' field included
        task = Task.objects.create(
            user=user,  # <--- FIX: Assigning the task to your admin/user
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=deadline,
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
            category=random.choice(categories),
            priority=random.choice(priorities)
        )

        # 4. Create Notes for the task
        for _ in range(random.randint(1, 3)):
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        # 5. Create SubTasks for the task
        for _ in range(random.randint(2, 4)):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

    print(f"Successfully populated {n} tasks with notes and subtasks for {user.username}!")

if __name__ == '__main__':
    populate(15)