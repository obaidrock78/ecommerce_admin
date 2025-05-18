# Use the official Python image as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app into the container
COPY . /app

# Create the media directory
RUN mkdir -p /app/media

# Set PYTHONPATH to the working directory
ENV PYTHONPATH=/app

# Expose port 8000 to allow access to the service
EXPOSE 8000

# Run Alembic migrations before starting the FastAPI app
# This assumes you have your Alembic configuration file (alembic.ini) and migration scripts in place
# CMD statement is modified to run Alembic migration and then start FastAPI
CMD ["bash", "-c", "alembic upgrade head && python app/main.py"]