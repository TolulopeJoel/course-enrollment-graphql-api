FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize the database and then run the Flask application
CMD ["sh", "-c", "flask init-db && python -m flask run --host=0.0.0.0 --port=3000"]
