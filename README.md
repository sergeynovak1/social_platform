# social_platform

### Run 
```shell
alembic upgrade head
uvicorn src.main:app --reload
celery -A src.tasks.tasks:celery worker --loglevel=INFO --pool=solo
celery -A src.tasks.tasks:celery flower
pytest -v tests/
```