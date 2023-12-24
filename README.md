### Setup

#### Preparing your enviroment

1. You must need to have Python installed on your computer (I suggest you install from an enviroment manager like conda, virtualenv, pyenv, etc)
2. Install project dependencies from root project and at terminal run 
```pip install -r requirements.txt```

3. At first time you must create you tables (run once)
```./tools/create_tables.sh```
During this process the admin account will be created and you must need an e-mail and password when you asked.
If you skip this step, you need create admin account manually using
```python manage.py createsuperuser```

**Extra (trial)**
If your are using for trial purpose, you can populate the database, copy populate.py at tools directory to project root directory than run
```python populate.py```
Atfer tests, recreate the database running command at step 3 (above).

#### Setting your enviroment variables
1. Duplicate a env_example file, then rename it to .env
2. Create a new secret key using secret_key_generater.py (see tools directory)
3. Using your favorite text editor open .env file
4. Copy the new secret key for SECRET_KEY option at .env file
5. Change DEBUG option at your convinience, True for development or False for deploy
6. Set ALLOWED_HOSTS option at your convinience ([please read ALLOWED_HOSTS section from Django website](https://docs.djangoproject.com/en/5.0/ref/settings/))
7. Save .env
8. Move .env for makemake directory (application)