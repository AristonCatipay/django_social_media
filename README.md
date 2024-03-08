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

### Install Dependencies

Install Pipenv
```bash
pip install pipenv
```

Activate Virtual Environment
```bash
pipenv shell
```

Install Dependencies
```bash
pipenv install
```

Migrate
```bash
python manage.py migrate
```

Start the server
```bash
python manage.py runserver
```

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)