FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
#CMD ["tail", "-f", "/dev/null"]
CMD ["python", "-m", "flask", "--app", "flaskr", "run", "--debug", "--host=0.0.0.0"]