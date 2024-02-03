FROM python:3.9-alpine3.13
COPY . .
RUN pip install -r /Requirements.txt
RUN /usr/local/bin/pip install --upgrade pip
EXPOSE 8001
CMD ["python","manage.py","runserver","0.0.0.0:8001"]