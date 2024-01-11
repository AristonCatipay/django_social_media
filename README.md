![Connectify](/readme_images/connectify_desktop.png)
# Connectify - a Social Media Application

Connectify is a Django social media application where users can their friends and family.

## Run Locally

To use this application you have to clone this repository using git bash.

### Clone the repository
- Open the directory you want this application to be cloned. 
- Open git bash.

```bash
git clone https://github.com/AristonCatipay/django_social_media.git
```

### Install Dependencies using `requirements.txt`
Install project dependencies
```bash
pip install -r requirements
```

### Install Dependencies
Note: If there is an available `requirements.txt` you can skip this.

Activate virtual environment
```bash
pipenv shell
```

Install Django
```bash
pipenv install django
```

Install MySQL Client
```bash
pipenv install mysqlclient
```

Install Pillow
```bash
pipenv install pillow
```

Install Tailwind
```bash
pipenv install django-tailwind
```

Install Django Tailwind Reload
```bash
pipenv install django-tailwind[reload]
```

Create a database named 'django_social_media' 
using your RDMS of choice (in this case using XAMPP Server).

![Create_a_database](/readme_images/xampp_create_database.png)

Edit your database configuration in the settings.py.
![Database_Configuration](/readme_images/change_database_settings.png)

Migrate
```bash
python manage.py migrate
```

Start the server
```bash
python manage.py runserver
```

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)