# Under Construction


To Download Postgres Version 10: 

(https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Install It 

1. Open cmd prompt
2. Write psql postgres postgres -> "connect to the database named 'postgres' with the user 'postgres'". 'postgres' is the default root user name for the database.
3. create an new database : CREATE DATABASE projectrestro;
4. Connect to that database: \c projectrestro;
5. Create a new user that has permissions to use that database: CREATE USER admin WITH PASSWORD 'password';
6. Give the new user all privileges on new db: GRANT ALL PRIVILEGES ON DATABASE projectrestro TO admin;
7. disconnect from db : \q;


In accounts comment out signals.py and decorators.py and in views.py comment out the decorators (@unauthenticated_user)

run :  
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser
4. go to localhoast:8000/admin 
5. create two group admin and customer (No Caps) 
6. give superuser the group admin
7. uncomment eveything you did earlier
