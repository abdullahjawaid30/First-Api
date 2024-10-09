FROM python:3.12.2
EXPOSE 500
WORKDIR /app
COPY . .
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

CMD ["flask", "run", "--host", "0.0.0.0"]


