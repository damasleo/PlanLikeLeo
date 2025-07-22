
# Student Planner - Django Web Application

A comprehensive web application designed to help university students manage their academic life effectively. Built with Django, this application provides task management, schedule planning, note-taking, and user authentication features.

## 🎯 Project Overview

This Student Planner application is designed for 1st-year software engineering students as an academic project. It demonstrates the implementation of a full-stack web application using Django framework with modern UI/UX design principles.

## ✨ Features

### 🔐 User Authentication
- User registration and login system
- Secure password management
- User profile management

### 📊 Dashboard
- Overview of today's tasks
- Weekly task summary
- Upcoming tasks display
- Recent notes preview
- Quick action buttons

### 📝 Task Management
- Create, edit, and delete tasks
- Task categories (Homework, Exam, Project, Assignment, Study, Other)
- Task status tracking (To Do, In Progress, Done)
- Due date management
- Real-time status updates via AJAX

### 📅 Schedule Management
- Weekly timetable view
- Add/edit class schedules
- Time slot management
- Room and instructor information
- Day-wise organization

### 📔 Notes Section
- Create and manage personal notes
- Rich text content
- Note organization and search
- Timestamp tracking

### 📱 Responsive Design
- Mobile-friendly interface
- Bootstrap 5 framework
- Modern gradient design
- Interactive UI elements

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Authentication**: Django's built-in auth system

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Student-Planner
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
Open your web browser and navigate to:
- Main Application: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 🚀 Usage Guide

### Getting Started
1. **Register an Account**: Visit `/register` to create a new account
2. **Login**: Use your credentials to access the dashboard
3. **Explore Features**: Navigate through the different sections using the top navigation bar

### Managing Tasks
1. **Create Tasks**: Click "Add New Task" from the tasks page
2. **Set Details**: Fill in title, description, due date, category, and status
3. **Track Progress**: Update task status using the dropdown menu
4. **Organize**: Use categories to group related tasks

### Managing Schedule
1. **Add Classes**: Click "Add Class" from the schedule page
2. **Set Times**: Specify day, start time, end time, and location
3. **View Weekly**: See your complete weekly timetable
4. **Manage**: Edit or delete schedule items as needed

### Taking Notes
1. **Create Notes**: Click "Add New Note" from the notes page
2. **Write Content**: Add title and detailed content
3. **Organize**: All notes are automatically timestamped
4. **Access**: View and edit notes from the notes section

## 📁 Project Structure

```
Student-Planner/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── student_planner/         # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── planner/                 # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # Database models
│   ├── urls.py              # App URL patterns
│   ├── views.py             # View functions
│   ├── templatetags/        # Custom template tags
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   └── planner/
│       ├── base.html        # Base template
│       ├── dashboard.html   # Dashboard page
│       ├── login.html       # Login page
│       ├── register.html    # Registration page
│       ├── tasks.html       # Task management
│       ├── schedule.html    # Schedule management
│       ├── notes.html       # Notes management
│       └── profile.html     # User profile
└── static/                  # Static files
    ├── css/
    │   └── style.css        # Custom styles
    └── js/
        └── script.js        # JavaScript functionality
```

## 🗄️ Database Models

### Task Model
- User (ForeignKey)
- Title (CharField)
- Description (TextField)
- Due Date (DateField)
- Category (CharField with choices)
- Status (CharField with choices)
- Created/Updated timestamps

### ScheduleItem Model
- User (ForeignKey)
- Day of Week (CharField with choices)
- Start Time (TimeField)
- End Time (TimeField)
- Subject (CharField)
- Room (CharField, optional)
- Instructor (CharField, optional)

### Note Model
- User (ForeignKey)
- Title (CharField)
- Content (TextField)
- Created/Updated timestamps

## 🎨 Design Features

### Color Scheme
- Primary: Gradient blues (#667eea to #764ba2)
- Success: Gradient cyan (#4facfe to #00f2fe)
- Danger: Gradient pink (#fa709a to #fee140)
- Notes: Gradient purple (#f093fb to #f5576c)

### Responsive Design
- Mobile-first approach
- Bootstrap grid system
- Flexible card layouts
- Touch-friendly interface

### Interactive Elements
- Hover effects on cards
- Smooth transitions
- Loading animations
- Real-time status updates

## 🔧 Customization

### Adding New Task Categories
Edit `planner/models.py` and add new choices to the `CATEGORY_CHOICES` list in the Task model.

### Modifying Color Scheme
Update the CSS variables in `static/css/style.css` to change the application's color scheme.

### Adding New Features
The modular structure makes it easy to add new features by:
1. Creating new models in `models.py`
2. Adding views in `views.py`
3. Creating templates in `templates/planner/`
4. Updating URL patterns in `urls.py`

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty planner
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Issues**
   ```bash
   python manage.py flush  # Clear database
   python manage.py migrate  # Re-run migrations
   ```

### Debug Mode
For development, ensure `DEBUG = True` in `settings.py`. For production, set to `False`.

## 📝 License

This project is created for educational purposes as part of a 1st-year software engineering course.

## 👨‍💻 Development

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Testing
To run tests (when implemented):
```bash
python manage.py test
```

### Deployment
For production deployment:
1. Set `DEBUG = False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Use a production WSGI server (Gunicorn)

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome through:
1. Issue reporting
2. Feature requests
3. Code improvements

## 📞 Support

For questions or issues related to this academic project, please refer to the course instructor or create an issue in the project repository.

---

**Note**: This application is designed for educational purposes and demonstrates fundamental web development concepts using Django framework. 
