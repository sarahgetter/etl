# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables for database credentials
ENV DB_USER=your_db_username
ENV DB_PASS=your_db_password

# Run etl_script.py when the container launches
CMD ["python", "etl_script.py", "--config", "config.yaml"]
