set -o errexit
set -o xtrace  # prints each command before executing

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
