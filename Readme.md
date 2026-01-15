# Quiz Master - Online Quiz Management System

## Description

This project is a web-based quiz management system called **Quiz Master**. It allows users to register, log in, and take quizzes organized by subjects and chapters. Admins can manage subjects, chapters, quizzes, and questions, while users can view their scores and progress.

## Technologies Used

- **Flask**: Web framework for routing, templates, and backend logic
- **Flask-SQLAlchemy**: Database ORM to manage models and relationships
- **Flask-WTF**: Form handling and validation
- **SQLite**: Database to store user, quiz, and score data
- **Bootstrap**: Responsive and user-friendly UI design
- **Flask-Login**: User authentication and session management
- **Chart.js**: Interactive charts for progress visualization

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps
1. Clone the repository
   ```bash
   git clone <repository-url>
   cd 23f3002567_quiz_master
   ```

2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Access at `http://localhost:5000`

### Default Admin Credentials
- **Email**: admin
- **Password**: admin123

## Architecture & Features

### Architecture
The project follows the **MVC (Model-View-Controller)** architecture:
- **Models**: Defined in `models.py` using Flask-SQLAlchemy for database interactions
- **Views**: HTML templates in the `templates/` folder, styled with Bootstrap
- **Controllers**: Routes defined in `routes.py` handle user requests and business logic

### Features
1. **User Authentication**: Secure login and registration using Flask-Login and Flask-WTF
2. **Admin Management**: Admins can create, edit, and delete subjects, chapters, quizzes, and questions
3. **Quiz Attempt and Scoring**: Users can attempt quizzes, and their scores are calculated and stored
4. **Progress Tracking**: Users can view their scores and progress through interactive charts using Chart.js
5. **Search Functionality**: Users can search for subjects, chapters, quizzes, and other resources (admin only)
6. **Responsive Design**: The application is fully responsive, ensuring usability across all devices

## Database Models

- **User**: Stores user profile, credentials, and qualification information
- **Subject**: Organizes content into subjects
- **Chapter**: Groups quizzes within subjects
- **Quiz**: Contains quiz metadata, timing, and questions
- **Questions**: Individual quiz questions with multiple-choice options
- **Scores**: Tracks user performance and quiz attempts

## Project Structure

```
├── app.py              # Flask application initialization
├── config.py           # Configuration settings
├── models.py           # SQLAlchemy database models
├── routes.py           # Flask route handlers
├── forms.py            # WTForms form definitions
├── requirements.txt    # Python dependencies
├── instance/
│   └── quiz.db        # SQLite database
└── templates/         # HTML templates
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── chapters.html
    ├── quizzes.html
    ├── theQuiz.html
    ├── scores.html
    └── ...
```

## How to Use

### For Users
1. Register with email and password
2. Log in to your account
3. Browse subjects and chapters
4. Attempt quizzes and submit answers
5. View your scores and performance analytics

### For Admins
1. Log in with admin credentials
2. Create and manage subjects
3. Add chapters to subjects
4. Create quizzes with questions
5. Define multiple-choice options and correct answers
6. Monitor user scores and attempt history