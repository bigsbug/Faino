
echo -e "\n$(tput bold setaf 6)Collect static files ..."
python3 manage.py collectstatic --noinput 

echo -e "\n$(tput bold setaf 6)Makemigrations and apply migrates ... "
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput 

echo -e "\n$(tput bold setaf 6)Run uvicorn server ... "
uvicorn config.asgi:application --reload --host ${DJANGO_IP} --port ${DJANGO_PORT} --workers ${WORKERS_COUNT_UVICORN} ${EXTRA_UVICORN_ARGS}