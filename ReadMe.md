# Plasma Donor Finder COVID19
##### UNDER DEVELOPMENT
###### Check Issue tracker for updates
This is a simple website used to connect Donors of Plasma and Hospitals for the treatment of COVID19. Plasma therapy is recently started in India and this website will act as a platform to connect nearby donor with hospitals the require plasma.

## Steps for local development

1. Clone the repository by running the following command in the terminal :
   ```shell
   git clone https://github.com/abbasidaniyal/PlasmaDonorFinder.git
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
   cd PlasmaDonorFinder   
   ```
      
5. Install dependencies by running the following command:
   ```shell
   pip install -r requirements.txt
   ```
6. Run the Django standard runserver steps:
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
 Your website will be up and running at http://localhost:8000