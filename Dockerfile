FROM python:3.11

WORKDIR .
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

ENV DB_URL='mysql://user:pass@host.docker.internal:3307/wallets'

ENV PYTHONUNBUFFERED=1

RUN alembic upgrade head

CMD ["python3.11", "app/manage.py", "runserver", "0.0.0.0:8080" ]