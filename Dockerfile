FROM python:3

RUN apt-get update \
    && apt-get install python3 \
        python3-pip

WORKDIR /usr/src/app
COPY AnnoMathTeX/requirements.txt ./
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip install -r requirements.txt
RUN /annomathtex/manage.py runserver
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]