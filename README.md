
# Faino 
![enter image description here](https://img.shields.io/badge/License-GPL--3.0-green) ![enter image description here](https://img.shields.io/github/commit-activity/y/bigsbug/faino)

## Description
 **Faino** is a platform for IoT devices, based on python and Django frameworks, Faino it’s an alternative for Thingsboard and Toya web servers and it provides some exciting feature

## Table of Contents
 - [Description](#description)
 -  [Features](#features)
 - [Requirements](#requirements)
 -  [Installation](#installation) 
 - [Config](#configs)
	- [Django config](#dajngo-config)
	- [Uvicorn config](#uvicorn-config)
	- [Postgres config](#postgres-config)
 -  [Usage](#usage) [ Unvaliable ]
 -  [ToDo](#todo)

## Features
 - Connect devices over WebSocket
 - Accessing devices with a powerful Restful-API
 - Offers some permission like **OWNER**, **ADMIN**, **MEMBER**
 - Registering unlimited devices to the server
 - Possession transition of devices to other users
 - Connect devices to the server with token authentication
 - Provide permissions to other users to accessing to your devices
 - Two-step authentication
 - Send customize commands to devices over Websocket with HTTP API
 - Create Customize permissions for your users to access your devices
 - Create a queue of commands to send to devices
 - Check the status of devices in real-time
 - Update source code IoT devices over the server in real-time
 - Providing a profile per user for each device
 - Record activities of users and devices
 ## Requirements
the only thing you needs is to install the below software:
 - [Docker](https://docs.docker.com/get-docker/)
 - [Docker Compose](https://docs.docker.com/compose/install/)

 ## Installation

### Development Setup:
the first thing is editing some of the config files to complete the setup. edit the EMAIL CONFIG and SECRET_KEY from [/config/django.dev.env](#dajngo-config)

**[SECRET_KEY](#dajngo-config) :**  We recommend generating a new secret key and filling it with that. how generate a secret key? the easiest way to generate is this website [djecrety.ir](https://djecrety.ir/).
or following the [official document of python](https://docs.python.org/3/library/secrets.html) to generate the new secret key.

**[EMAIL CONFIG](#dajngo-config):** in this section, you should config your email settings this config is used for sending some emails like activation codes and verifying codes to users. for more information how to fill this section you can read this page

**Tip:** The place all development config is /config/ folder with pattern *[config-name].dev.env*

after complate the configs your should run this script in your terminal :

    $ ./install-service.sh
this command build the images and run the containter
 
there are some scripts available for convenience like :

**start-service.dev.sh :**
 - > Starting Faino development environment again, after changing some of the configs or when is stopping

**stop-service.dev.sh :**
 - > Stoping Faino Development Environment

**django-manager.sh :**
 - > alternative for manage.py of Django but in the container you can use it like normal manage.py

## Configs:
 the config files are used by the Faino and Docker services, there are some environment files and some python files to config how to work and customize the project with your needs
 
 #### dajngo config:
|Config Name|Description|Required|
|--|--|--|
|REQUIREMENTS_FILE|The path of requirements.txt file |Yes
|DJANGO_SETTINGS_MODULE|The path of django settings [see more](https://docs.djangoproject.com/en/4.0/topics/settings/#envvar-DJANGO_SETTINGS_MODULE)|Yes
|SECRET_KEY|Secret key of django settings [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key)|Yes
|ALLOWED_HOSTS|List of allowed host in django [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts)|Yes
|DEBUG|Status of debuging [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#debug)|Yes
|APPEND_SLASH|Status of appending slash in the end url [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#append-slash)|No
|EMAIL_USE_TLS|Status of using tls for email service [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#email-use-tls)|No
|EMAIL_HOST|Email provider host [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host)|Yes
|EMAIL_PORT|Email port [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#email-port)|Yes
|EMAIL_HOST_USER|Email address [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-user)|Yes
|EMAIL_HOST_PASSWORD|Email password [see more](https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-password)|Yes

#### uvicorn config:
|Config Name|Description|Required|
|--|--|--|
|DJANGO_IP|Django bind IP in the django service|Yes
|DJANGO_PORT|Django port bhind in the django service|Yes
|WORKERS_COUNT_UVICORN|Workers count of Uvicorn [see more](https://www.uvicorn.org/settings/#production)|Yes
|EXTRA_UVICORN_ARGS|Pass extra config to Uvicorn [see more](https://www.uvicorn.org/settings/)|No

#### postgres config:
|Config Name|Description|Required|
|--|--|--|
|POSTGRES_DB|Name of Postgres DB|Yes
|POSTGRES_USER|User of Postgres DB|Yes
|POSTGRES_PASSWORD|Password of Postgres DB|Yes


**Tip  :**
>Some of the Configs by default are available and you edit some of those.

**Config Place** :
>you can find here available configs: **Config/***[name config]****.***[mod]**.env**

## TODO

 - [ ] Create Dashboard
 - [ ] Fixing tests of API
 - [x] Provide bash script to direct accessing to manage.py of Django in container
 - [ ] Provide logs file of each service in the *logs* folder
 - [x] Create Development environment
 - [ ] Create contribute guideline
 - [ ] Document API app
 - [ ] Document WebServer App
 - [ ] Document AuthSystem App
 - [ ] Document Quickstart
 - [x] Section Development
