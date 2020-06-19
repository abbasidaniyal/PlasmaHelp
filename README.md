# Plasma Help COVID19
 
![GitHub issues](https://img.shields.io/github/issues/abbasidaniyal/PlasmaHelp) ![GitHub](https://img.shields.io/github/license/abbasidaniyal/PlasmaHelp) ![Django CI](https://github.com/abbasidaniyal/PlasmaHelp/workflows/Django%20CI/badge.svg?branch=develop)

This is a simple website used to connect Donors of Plasma and Hospitals for the treatment of COVID19. Plasma therapy is recently started in India and this website will act as a platform to connect nearby donor with hospitals the require plasma.

## System Architecture
Deployment system architecture
![PlasmaHelp](https://plasmahelp.org/static/img/system_arch_1.png)

## Google Maps API

1. This project uses google maps API. Go to https://console.cloud.google.com/ and create a new project.
2. Create an API key
3. Activate the following services for the API key

- Geolocation API
- Maps Javascript API
- Places API

Add the API KEY to the .env file. (Follow the installation below)

## Steps for local development manually

1. Clone the repository by running the following command in the terminal :

   ```shell
   git clone https://github.com/abbasidaniyal/PlasmaHelp.git
   ```

2. Install virtualenv. Run the following commands in terminal:
   ```shell
   pip install virtualenv
   ```
3. Create a virtual environment and activate it.

   ```shell
   python -m venv <path>/<env_name>
   source <path>/<env_name>/bin/activate (Linux)
   <path>\<env_name>\Scripts\activate (Windows)
   ```

   The environment will be created in the specified path.

4. navigate into the repository by running the following command in terminal:
   ```shell
   cd plasmahelp
   ```
5. Install dependencies by running the following command:
   ```shell
   pip install -r requirements.txt
   ```
5. Create a .env file using the .env.sample format in the root directory 
6. Run the Django standard runserver steps:
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
   Your website will be up and running at http://localhost:8000

## Using Docker Compose

1.  Create a .env file and a .env_postgis file from the .env.sample file and .env_postgis.sample. Simply copy the contents and setup required environment variables.

    Note : Make sure that the db settings in both the files are same.

2.  Install Docker and Docker-compose in your system. Use the following commands.

    For docker : https://docs.docker.com/get-docker/

    For docker-compose : https://docs.docker.com/compose/install/

3.  Create an empty directory named `postgres`. This will be the volume mount point for the db.
    ```shell script
    mkdir postgres
    ```
4.  If you simply wish to run the project, use the following command:

    ```shell script
     docker-compose up
    ```

5.  If you want to develop using auto reload, use

    ```shell script
     docker-compose up db
    ```

    This will start the database container. Then you can start django by running `./django_setup.sh`

### Contribution

1.  Install pre-commit hooks : Already in requirements.txt (pip install pre-commit)
2.  Run the folloing to install pre-commit

    ```shell script
    pre-commit install
    ```
