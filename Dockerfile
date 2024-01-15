# Use the official Python image as the base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /Alemeno_Backend_Assign

# Copy the requirements file to the working directory
COPY requirements.txt /Alemeno_Backend_Assign/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire application to the working directory
COPY . /Alemeno_Backend_Assign/

# Run migrations and collect static files (customize based on your needs)
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Alemeno_Backend_Assign.wsgi:application"]
