FROM python:3.12-alpine

WORKDIR /app
ENV PYTHONPATH=/app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
