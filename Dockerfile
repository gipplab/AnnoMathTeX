FROM python:3

WORKDIR /usr/local
COPY ./ AnnoMathTeX
WORKDIR ./AnnoMathTeX
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip3 install -r requirements.txt
RUN mkdir -p ./usr/local/nltk_data
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python3 annomathtex/manage.py migrate
EXPOSE 8000
CMD ["python3", "annomathtex/manage.py", "runserver", "0.0.0.0:8000"]
