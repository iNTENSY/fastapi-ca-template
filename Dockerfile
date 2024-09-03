FROM python:3.11

WORKDIR /core

RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app.presentation.entrypoint:app_factory", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]