# Use an official Python runtime as the base image
FROM python:3.7

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirement.txt .
RUN pip install -r requirement.txt

# Copy the project files into the container
COPY . .

# Expose the port your application will run on
EXPOSE 8001

# Start the application with Uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]