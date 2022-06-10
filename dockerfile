######################## BASE PYTHON IMAGE ########################
FROM python:3.9-alpine
# install psycopg2 dependencies
RUN apk update \
    && apk add  --no-cache postgresql-dev gcc python3-dev musl-dev \
    &&  pip install --no-cache-dir psycopg2-binary 
    # FROM base-python-dev
    # WORKDIR /app
    # COPY . /app/
    # RUN pip install --upgrade pip && pip install -r requirements.txt 
    # ENV server-port=8000
    # CMD [ "python3" ,"manage.py" , "runserver" , server-port ]

