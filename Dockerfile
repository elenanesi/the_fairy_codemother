# Use Playwright's official Python image
FROM mcr.microsoft.com/playwright/python:v1.41.1

EXPOSE 8080

# Set the working directory
WORKDIR /app

# Copy the Python dependencies file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Set display environment variable for Xvfb
# ENV DISPLAY=:99

# Copy the application's files to the container
COPY . /app

# Initialize Xvfb and run the Python script
# CMD Xvfb :99 -screen 0 1024x768x16 & sleep 2; python3 app.py

# Run app.py when the container launches
CMD ["python", "app.py"]
