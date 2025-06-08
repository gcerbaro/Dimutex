FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 6000

CMD ["python", "shared.py"]