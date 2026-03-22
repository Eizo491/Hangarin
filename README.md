# Hangarin: Task Management System

Hangarin is a modern, web-based task management application designed to help users organize their workflows with a clean, glassmorphism-inspired interface. Built with Django 5.2.12, it prioritizes system security, user experience, and efficient data handling.

## Features

- **User Authentication**: Secure sign-up and login system using Django's built-in authentication framework.
- **Glassmorphism UI**: A high-end aesthetic featuring violet gradients, frosted glass effects, and responsive design.
- **CRUD Functionality**: Create, Read, Update, and Delete tasks with ease.
- **Task Organization**: Categorize tasks and assign priority levels to manage urgency effectively.
- **Deadline Tracking**: Integrated date tracking to ensure tasks are completed on schedule.
- **Animate-on-Load**: Smooth CSS animations for a polished feel during navigation.

## Tech Stack

- **Backend**: Python 3.11, Django 5.2.12
- **Frontend**: HTML5, CSS3 (Custom Variables), Bootstrap 5, Font Awesome
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Tools**: Django Widget Tweaks, Jazzmin (Admin Customization)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/hangarin_project.git](https://github.com/yourusername/hangarin_project.git)
   cd hangarin_project

2. **Set up a virtual environment**

    Bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

3. **Install dependencies**

    Bash
    pip install django django-widget-tweaks django-jazzmin
    
4. **Run Migrations**

    Bash
    python manage.py makemigrations
    Note: If you encounter a FieldError regarding 'level' in Priority, ensure your models are migrated to the latest schema.

    Bash
    python manage.py migrate

5. **Start the Development Server**

Bash
python manage.py run server

Project Structure
hangarin_config/: Core project settings and URL configurations.

tasks/: Main application containing logic for task management, views, and forms.

templates/: HTML structures including the base.html and glass-styled auth screens.

static/: Custom CSS (style.css) and branding assets.

Future Enhancements
Implementation of Machine Learning for fraud analytics within task logs.

Real-time notifications for approaching deadlines.

Integration of a Tricycle Fare Calculator API for localized logistics (Palawan-specific).

Author
Lancesthur Keith S. Tapaya Information Technology Student | Web Developer & Designer

Palawan State University


---

### 💡 Tips for your Midterm Submission:
* **Screenshot Section**: Since we've worked hard on that violet glassmorphism look, I recommend adding a `Screenshots` folder to your repo and linking them in the README so your instructor sees the UI before even running the code.
* **The "Level" Fix**: Since we fixed the `FieldError` in `forms.py` by switching to `id`, your project should now run smoothly without needing to change your database.

**Would you like me to generate a `requirements.txt` file for you so you can easily share the projec