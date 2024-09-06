FROM python:3.11

WORKDIR /core

RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.presentation.entrypoint:app_factory", "--host", "0.0.0.0", "--port", "8000"]