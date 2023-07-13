FROM python:3

COPY . /FilmAPI
WORKDIR /FilmAPI
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8004
EXPOSE 8004