FROM python:3.11.3

RUN mkdir /var/www

RUN mkdir /var/www/fastapi_app

WORKDIR /var/www/fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000