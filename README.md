# Faino 
![enter image description here](https://img.shields.io/badge/License-GPL--3.0-green) 

**Faino** is a platform for IoT devices, based on python and Django frameworks, Faino it’s an alternative for Thingsboard and Toya web servers and it provides some exciting feature
### Features:
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
 
 ## Installation
 ### Configs:
 the config files are used from the Faino and Docker services there are some environment files and some python files to config how to work and customize the project with your needs
 
 #### dajngo config :
|Config Name|Description|Required|
|--|--|--|
|REQUIREMENTS_FILE|The path of requirements.txt file|Yes
|DJANGO_SETTINGS_MODULE|The path of django settings|Yes
|SECRET_KEY|Secret key of django settings|Yes
|ALLOWED_HOSTS|List of allowed host in django|Yes
|DEBUG|Status of debuging|Yes
|APPEND_SLASH|Status of appending slash in the end url|No
|EMAIL_USE_TLS|Status of using tls for email service|No
|EMAIL_HOST|Email provider host|Yes
|EMAIL_PORT|Email port|Yes
|EMAIL_HOST_USER|Email address|Yes
|EMAIL_HOST_PASSWORD|Email password|Yes

#### uvicorn config :
|Config Name|Description|Required|
|--|--|--|
|DJANGO_IP|Django bind IP in the django service|Yes
|DJANGO_PORT|Django port bhind in the django service|Yes
|WORKERS_COUNT_UVICORN|Workers count of Uvicorn|Yes
|EXTRA_UVICORN_ARGS|Pass extra config to Uvicorn|No

#### postgres config :
|Config Name|Description|Required|
|--|--|--|
|POSTGRES_DB|Name of Postgres DB|Yes
|POSTGRES_USER|User of Postgres DB|Yes
|POSTGRES_PASSWORD|Password of Postgres DB|Yes


**Tip  :**
>Some of the Configs by default are available and you edit some of those.

**Config Place** :
>you can find here available configs: **Config/***[name config]****.***[mod]***.env**

## TODO

 - [ ] Create Dashboard
 - [ ] Fixing tests of API
 - [ ] Provide bash script to direct accessing to manage.py of Django in container
 - [ ] Provide logs file of each service in the *logs* folder
 - [ ] Create Development environment
 - [ ] Create contribute guideline
 - [ ] Document API app
 - [ ] Document WebServer App
 - [ ] Document AuthSystem App
 - [ ] Document Quickstart
 - [ ] Section Development
