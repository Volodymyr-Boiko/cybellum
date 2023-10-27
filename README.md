To run the project:

    `docker-compose up`

To create migrations:
    `docker-compose exec -it app poetry run alembic revision --autogenerate`

To apply migrations:
    `docker-compose exec -it app poetry run alembic upgrade head`

To run test:
    `docker-compose exec -it app poetry run pytest`

To run black:
    `docker-compose exec -it app poetry run black app`

To run isort:
    `docker-compose exec -it app poetry run isort app`

To run pylint:  #TODO need to fix pylint, there are a lot of errors
    `docker-compose exec -it app poetry run pylint app`
   