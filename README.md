# Flask Chatbot Project

This is a simple Flask web application that serves as a chatbot interface. The application is structured to separate concerns between the backend logic, frontend presentation, and static assets.

## Project Structure

```
flask-app
├── app.py               # Main entry point for the Flask application
├── templates            # Directory for HTML templates
│   └── index.html      # Main page of the website
├── static              # Directory for static files
│   ├── style.css       # CSS styles for the website
│   └── script.js       # JavaScript for client-side functionality
├── requirements.txt     # Python dependencies for the project
├── .env                 # Environment variables for configuration
└── README.md            # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the root directory and add your configuration settings.

6. **Run the application:**
   ```
   python app.py
   ```

## Usage

Once the application is running, you can access it by navigating to `http://127.0.0.1:5000` in your web browser. The main page will load the chatbot interface.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.