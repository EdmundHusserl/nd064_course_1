FROM    python:3.8-slim-buster
EXPOSE  3111
WORKDIR /app
ADD     . .
RUN     pip3 install -r requirements.txt && python3 init_db.py
CMD     [ "python3", "app.py" ]
