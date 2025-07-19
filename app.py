# app.py (Modified for Render with Selenium)
from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service # Not needed if chromedriver is in PATH
import os
import time

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_super_secret_key_here')

# Selenium function, now integrated directly
def get_attendance_summary_selenium_integrated(username, password):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage') # Required for some environments

    # Explicitly set the binary and driver path, as they are installed via apt-get in Dockerfile
    options.binary_location = os.getenv("CHROME_PATH", "/usr/bin/chromium-browser")
    service_args = ['--verbose'] # For more logs from chromedriver

    # Pass the executable path directly to the service
    # driver = webdriver.Chrome(service=Service(os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromium-chromedriver")), options=options)
    # Simpler: If chromedriver is in PATH (which /usr/bin is), you might not need Service object directly
    # Just ensure it's in a location accessible by the PATH env variable.
    # In the Dockerfile, we put chromium-chromedriver in /usr/bin which is typically in PATH.
    driver = webdriver.Chrome(options=options)


    attendance_data = {
        "present": 0,
        "absent": 0,
        "percentage": 0.0,
        "message": "Failed to retrieve attendance.",
        "success": False
    }

    try:
        driver.get("https://samvidha.iare.ac.in/")
        time.sleep(5) # Give more time for initial page load

        username_field = driver.find_element(By.ID, "txt_uname")
        password_field = driver.find_element(By.ID, "txt_pwd")
        submit_button = driver.find_element(By.ID, "but_submit")

        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()
        time.sleep(7) # Give more time for login redirection

        if "login" in driver.current_url.lower() or "invalid" in driver.page_source.lower():
            attendance_data["message"] = "Login failed. Please check your credentials."
            return attendance_data
        print("✅ Logged in successfully.") # This will appear in Render logs

        attendance_url = "https://samvidha.iare.ac.in/home?action=course_content"
        driver.get(attendance_url)
        time.sleep(15) # *** EVEN MORE INCREASED SLEEP TIME for Render's slow free tier ***

        full_text = driver.find_element(By.TAG_NAME, "body").text
        normalized_full_text = full_text.upper().replace(" ", "").replace("\n", "").replace("\t", "")

        present_count = normalized_full_text.count("PRESENT")
        absent_count = normalized_full_text.count("ABSENT")
        total = present_count + absent_count

        attendance_data["present"] = present_count
        attendance_data["absent"] = absent_count

        if total > 0:
            percentage = round((present_count / total) * 100, 2)
            attendance_data["percentage"] = percentage
            attendance_data["message"] = f"Attendance retrieved! Present: {present_count}, Absent: {absent_count}, Percentage: {percentage}%"
            attendance_data["success"] = True
        else:
            attendance_data["message"] = "No attendance data found. This might indicate a problem with the page content or the scraping logic."
            attendance_data["success"] = True

    except Exception as e:
        attendance_data["message"] = f"An error occurred during attendance retrieval: {str(e)}. Check Render logs for details."
        attendance_data["success"] = False
        print(f"❌ Error in Selenium part: {e}")
    finally:
        driver.quit()
    return attendance_data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_attendance', methods=['POST'])
def get_attendance():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    print(f"Received request for attendance for user: {username}")
    # Call the integrated Selenium function
    attendance_results = get_attendance_summary_selenium_integrated(username, password)
    print(f"Selenium finished for {username}. Success: {attendance_results['success']}")

    return jsonify(attendance_results)

# This part is for local testing with 'python app.py'
if __name__ == '__main__':
    # Make sure to set FLASK_SECRET_KEY in your local .env
    # For local dev, you might need to comment out the driver options.binary_location
    # and use Service(ChromeDriverManager().install()) again, or install chromedriver manually.
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT', 5000))
