FROM python:3

WORKDIR /usr/src/app
COPY ./ AnnoMathTeX
WORKDIR ./AnnoMathTeX
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d ./nltk_data punkt
RUN python3 -m nltk.downloader -d ./nltk_data stopwords
RUN python3 -m nltk.downloader -d ./nltk_data averaged_perceptron_tagger
RUN python3 annomathtex/manage.py migrate
RUN python3 annomathtex/manage.py runserver
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
