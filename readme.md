Prerequisites for windows:
Python 3.6+
 - https://www.python.org/downloads/release/python-3105/
 
Pip
 - should be a part of Python installation
Psycopg PostgreSQL adapter
- pip install psycopg2


Docker 
- https://docs.docker.com/desktop/install/windows-install/
- download the Linux kernel update package (WSL2 for windows)
Pull the latest images for PostreSQL and pgadmin4
 - docker pull postgres
 - docker pull dpage/pgadmin4:latest

Navigate to main directory and run 
 - docker compose up 

Now, the environemnt is ready.

Go to localhost:5050
 - email: amin@admin.com
 - password: root

Create a new Server > my_db
 - host: pg_container 
 - port: 5432
 - username: root
 - password: root
 - run python main.py
 - navigate to Servers > my_db > Databases > Schemas > Tables and view data in final_table
