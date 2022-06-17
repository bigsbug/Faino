######################## BASE PYTHON IMAGE ########################
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV port=8000
ENV ip=0.0.0.0
ENV settings=settings.settings
ENV requirements=/src/requirements/dev.txt

EXPOSE ${port}

WORKDIR /src
COPY . .

RUN pip install --no-cache-dir -r ${requirements}

CMD python3 ./manage.py runserver ${ip}:${port} --settings=${settings}