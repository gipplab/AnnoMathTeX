FROM python:3

RUN apt-get update \ apt-get install python3-pip
WORKDIR /usr/src/app
COPY AnnoMathTeX/requirements.txt ./
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip install -r requirements.txt
COPY AnnoMathTeX .
RUN /annomathtex/manage.py migrate
RUN /annomathtex/manage.py runserver
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
