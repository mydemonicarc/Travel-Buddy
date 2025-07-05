Hello everyone!!
Travel Buddy
Your Ultimate Travel Companion
Travel Buddy is a user-friendly travel agency website built with Python, Flask, and Jinja2. Its primary goal is to empower users to browse captivating travel destinations, view diverse tour packages, and seamlessly connect with travel opportunities, demonstrating dynamic web content delivery.



✨ Features
Destination Discovery: Explore various travel destinations.

Search & Filter: Easily find destinations based on your preferences.

User Authentication: Secure login and registration.

Responsive Design: Works well on all devices.

🚀 Technologies Used
Backend: Python, Flask, SQLAlchemy

Frontend: Jinja2, HTML, CSS 

Database: SQLite

🛠️ Setup and Installation
Clone the repository:

git clone https://github.com/your-username/travel-buddy.git
cd travel-buddy

Install dependencies:

pip install -r requirements.txt

(Ensure you have a requirements.txt file from your project dependencies.)

Set up environment variables:
Create a .env file with FLASK_APP=app.py, FLASK_ENV=development, SECRET_KEY='your_secret_key', and DATABASE_URL='sqlite:///site.db'.

Initialize the database (if using Flask-Migrate):

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Run the application:

flask run

Access it at http://127.0.0.1:5000/.

🤝 Contributing
Feel free to contribute by forking the repository, creating a new branch, making your changes, and opening a Pull Request.

