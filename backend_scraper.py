from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def get_attendance_summary_selenium(username, password):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')  # Run in headless mode for server
    options.add_argument('--disable-gpu') # Recommended for headless
    options.add_argument('--window-size=1920,1080') # Set a window size for headless

    # Use webdriver_manager to automatically download/manage chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    attendance_data = {
        "present": 0,
        "absent": 0,
        "percentage": 0.0,
        "message": "Failed to retrieve attendance.",
        "success": False
    }

    try:
        driver.get("https://samvidha.iare.ac.in/")
        time.sleep(2)

        driver.find_element(By.ID, "txt_uname").send_keys(username)
        driver.find_element(By.ID, "txt_pwd").send_keys(password)
        driver.find_element(By.ID, "but_submit").click()
        time.sleep(3)

        # Basic check for successful login (you might need a more robust check)
        if "login" in driver.current_url.lower() or "invalid" in driver.page_source.lower():
            attendance_data["message"] = "Login failed. Please check your credentials."
            return attendance_data

        driver.get("https://samvidha.iare.ac.in/home?action=course_content")
        time.sleep(5) # Give page time to load content

        full_text = driver.find_element(By.TAG_NAME, "body").text

        present_count = full_text.upper().count("PRESENT")
        absent_count = full_text.upper().count("ABSENT")
        total = present_count + absent_count

        attendance_data["present"] = present_count
        attendance_data["absent"] = absent_count

        if total > 0:
            percentage = round((present_count / total) * 100, 2)
            attendance_data["percentage"] = percentage
            attendance_data["message"] = f"Attendance retrieved successfully! Present: {present_count}, Absent: {absent_count}, Percentage: {percentage}%"
            attendance_data["success"] = True
        else:
            attendance_data["message"] = "No attendance data found (0 present & absent combined)."
            attendance_data["success"] = True # Still a success, just no data

    except Exception as e:
        attendance_data["message"] = f"An error occurred during attendance retrieval: {str(e)}"
        attendance_data["success"] = False
    finally:
        driver.quit() # Always quit the driver

    return attendance_data

# Example of how to call it (for testing in isolation)
if __name__ == "__main__":
    # You would typically get these from environment variables or a secure configuration
    test_username = os.getenv("STUDENT_USERNAME")
    test_password = os.getenv("STUDENT_PASSWORD")

    if not test_username or not test_password:
        print("Please set STUDENT_USERNAME and STUDENT_PASSWORD environment variables for testing.")
    else:
        print(f"Attempting to get attendance for {test_username}...")
        result = get_attendance_summary_selenium(test_username, test_password)
        print("Result:", result)