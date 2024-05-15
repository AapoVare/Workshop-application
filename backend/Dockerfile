# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the app runs
EXPOSE 5000

# Set the environment variables if any
ENV FLASK_APP=new.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
# Run the application
CMD ["flask", "run"]
