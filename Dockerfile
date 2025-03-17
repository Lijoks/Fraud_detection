# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Expose the port the app runs on (adjust if needed)
EXPOSE 5000

# Define environment variable to tell Flask that it's running in production mode
ENV FLASK_ENV=production

# Run the application using gunicorn for better performance in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
