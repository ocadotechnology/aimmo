pip install -e .
python example_project\manage.py migrate --noinput
python example_project\manage.py collectstatic --noinput
python example_project\manage.py runserver %*