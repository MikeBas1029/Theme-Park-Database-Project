# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container and install dependencies
COPY ./backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add a non-root user to run the application
RUN adduser --disabled-password --no-create-home doe 

# Set the user to 'doe' for security reasons
USER doe 

# Copy the entire backend folder into the container
COPY ./backend/src /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["fastapi", "dev", "./main.py", "--port", "8000", "--host", "0.0.0.0"]