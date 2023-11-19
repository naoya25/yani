FROM python:3.10

RUN mkdir /var/www

COPY . /var/www

RUN pip install -r /var/www/requirements.txt

CMD ["python", "/var/www/app.py"]
