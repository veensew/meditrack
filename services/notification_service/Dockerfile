FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8004

#CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
CMD ["gunicorn", "--bind", "0.0.0.0:8004", "main:app"]