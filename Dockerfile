FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

COPY node/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "app.py"]