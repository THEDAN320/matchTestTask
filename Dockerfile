FROM python:3.10

RUN mkdir /TestTask
WORKDIR /TestTask

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]