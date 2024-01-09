# Base image
FROM python:3.9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements/dev-requirements.txt /app/

# Install project dependencies, without virtualenvironment
RUN pip install --upgrade pip && pip install -r dev-requirements.txt

# Copy the project code to the working directory
COPY . /app/

# Run migrations
RUN python manage.py migrate

# Expose port 8000 for the Django development server
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
