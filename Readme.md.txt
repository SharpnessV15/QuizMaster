Description
This project is a web-based quiz management system called quizzer. It allows users to register,
log in, and take quizzes organised by subjects and chapters. Admins can manage subjects,
chapters, quizzes and questions, while users can view their scores and progress
Technologies used
Flask: Used as the web framework to handle routing, templates, and backend logic.
Flask-SQLAlchemy: For database ORM to manage models and relationships.
Flask-WTF: For form handling and validation.
SQLite: Used as the database to store user, quiz, and score data.
Bootstrap: For responsive and user-friendly UI design.
Flask-Login: For user authentication and session management.
Architecture and Features
Architecture: The project follows the MVC (Model-View-Controller) architecture:
● Models: Defined in models.py using Flask-SQLAlchemy for database interactions.
● Views: HTML templates in the templates folder, styled with Bootstrap.
● Controllers: Routes defined in routes.py handle user requests and business logic.
Features:
1. User Authentication: ◦ Secure login and registration using Flask-Login and Flask-WTF.
2. Admin Management: ◦ Admins can create, edit, and delete subjects, chapters, quizzes, and
questions.
3. Quiz Attempt and Scoring: Users can attempt quizzes, and their scores are calculated and
stored.
4. Progress Tracking: Users can view their scores and progress through interactive charts
using Chart.js.
5. Search Functionality: Users can search for subjects, chapters, quizzes, and other users
(admin only).
6. Responsive Design: The application is fully responsive, ensuring usability across devices.