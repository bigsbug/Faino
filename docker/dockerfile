######################## BASE PYTHON IMAGE ########################
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ARG REQUIREMENTS_FILE

WORKDIR /src
COPY . .

RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

