from flask import Flask, request, jsonify, render_template
from backend_scraper import get_attendance_summary_selenium # Import your Selenium function
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
# For production, set a strong secret key from environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_super_secret_key_here')

@app.route('/')
def index():
    """Renders the main HTML page for the college website."""
    return render_template('index.html')

@app.route('/get_attendance', methods=['POST'])
def get_attendance():
    """
    API endpoint to retrieve attendance.
    Expects JSON with 'username' and 'password'.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    # In a real application, you would add more security:
    # 1. Rate limiting to prevent brute-force attacks.
    # 2. Input validation and sanitization.
    # 3. Consider not passing raw passwords if an alternative authentication flow exists.

    # Execute the Selenium scraper
    print(f"Received request for attendance for user: {username}")
    attendance_results = get_attendance_summary_selenium(username, password)
    print(f"Selenium finished for {username}. Success: {attendance_results['success']}")

    return jsonify(attendance_results)

if __name__ == '__main__':
    # In a production environment, use a production-ready WSGI server like Gunicorn or uWSGI
    # For development:
    app.run(debug=True, port=5000)