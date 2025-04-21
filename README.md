📽️ BookMySpot – Movie Booking Website
BookMySpot is a movie ticket booking web application built using Python Flask for the backend and HTML, CSS, Bootstrap, and JavaScript for the frontend. It enables users to browse and book tickets for movies across different genres and languages.

📁 Project Structure
css
BookMySpot/
├── Instance/
│   └── database.db
│
├── Website/
│   ├── static/
│   │   ├── Bollywood_Poster/
│   │   ├── CSS/
│   │   ├── Hollywood_Poster/
│   │   ├── JS/
│   │   ├── Pollywood_Poster/
│   │   ├── Upcoming/
│   │   └── Webimg/
│   │
│   └── Templates/
│       ├── Base.html
│       ├── home.html
│       ├── login.html
│       ├── sign_up.html
│       ├── email_otp.html
│       ├── reset_password.html
│       ├── search_results.html
│       ├── [Movie Booking Pages]
│       └── [Upcoming Movies Pages]
│
├── __intit__.py
├── auth.py
├── database.db
├── email_otp.py
├── models.py
├── views.py
└── main.py
🛠 Technologies Used
Backend Framework: Python Flask
Frontend: HTML, CSS, Bootstrap, JavaScript
Database: SQLite (database.db)
Authentication: Flask-Login, OTP email verification
Mailing: Flask-Mail
Other Dependencies:
Flask
Flask-Login
Flask-SQLAlchemy
Flask-Mail
requests

🚀 Features
✅ User Sign Up & Login (with email OTP)

🎫 Book movies from Bollywood, Hollywood, and Pollywood categories

🔍 Search for movies

📅 View upcoming movies

🔒 Secure session handling via Flask-Login

📧 Email-based OTP verification for secure sign-up/reset

🧪 Development Environment

Item	Details
Port	5000
Base URL	http://127.0.0.1:5000
Code Editor	VS Code
Python Version	Latest
Package Manager	None (manual pip install)

▶️ Running the Project Locally
Clone the repository
git clone https://github.com/your-username/BookMySpot.git
cd BookMySpot
Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install required packages
pip install Flask Flask-Login Flask-SQLAlchemy Flask-Mail requests
Run the Flask app
python main.py
Open in your browser
Visit http://127.0.0.1:5000

📦 Folder/Component Descriptions

Folder/File	Description
Instance/database.db	SQLite database file storing user and movie data
Website/static/	Static assets: posters, images, CSS, JS
Website/Templates/	HTML templates rendered by Flask
main.py	Entry point for Flask application
views.py	Routes and rendering logic
auth.py	Handles user login, signup, and sessions
email_otp.py	OTP generation and email sending logic
models.py	SQLAlchemy ORM models
