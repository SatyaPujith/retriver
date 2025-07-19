# Use a base image with Python and Ubuntu for apt
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV PORT 10000 # Render's default port

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libu2f-udev \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxshmfence6 \
    libxtst6 \
    xdg-utils \
    # Clean up APT cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Chrome to PATH and ensure it's found
ENV CHROMEDRIVER_PATH /usr/bin/chromium-chromedriver
ENV CHROME_PATH /usr/bin/chromium-browser

# Create a non-root user for security (recommended practice)
# Render might run as root by default, but if you switch, this is good.
RUN adduser --disabled-password --gecos '' appuser
USER appuser
WORKDIR /home/appuser/app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port
EXPOSE $PORT

# Command to run the application using Gunicorn
# Use 0.0.0.0 to bind to all network interfaces inside the container
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
