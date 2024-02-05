FROM python:3.9-alpine3.13
WOKDIR /app
COPY ./PythonGuides .
RUN pip install -r /Requirements.txt
RUN /usr/local/bin/pip install --upgrade pip
VOLUME /app/db_data
RUN python manage.py migrate
EXPOSE 8001
CMD ["python","manage.py","runserver","0.0.0.0:8001"]
