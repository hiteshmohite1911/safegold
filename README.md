# safegold
Safe Gold assessment

This project is create in FastAPI framework.

Prequisites:-
  Python3.8
  MySQL

Steps:-
  - Create a python virtual enviornment
  - Install all the Python libraries from requirements.txt
  - Run Alembic commands to create tables as per models created in models folder
    - alembic init
    - alembic revision --autogenerate -m "message"
    - alembic upgrade head
  - One small manual process to insert two records in Roles table, after tables are created
    - insert into roles (id,name) values (1,'Admin'),(2,'User');
  - Now you can run FastAPI project by running command - python main.py
  - You can access Swagger API documentation and make use of all APIs
