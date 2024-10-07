FROM python:3.12.2

WORKDIR /app

# Install Flask
RUN pip install flask

# Copy the current directory contents into the container at /app
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host", "0.0.0.0"]

