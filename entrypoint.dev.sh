echo -e "\n$(tput bold setaf 6)Makemigrations and apply migrates ... "
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput 

echo -e "\n$(tput bold setaf 6)Collect static files ..."
python3 manage.py collectstatic --noinput 


echo -e "\n$(tput bold setaf 6)Run gunicorn development server ... "
gunicorn --reload -k uvicorn.workers.UvicornWorker  -b ${DJANGO_IP}:${DJANGO_PORT} --workers ${WORKERS_COUNT} ${EXTRA_ARGS}  config.asgi:application 