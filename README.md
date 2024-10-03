# Restaurant Kitchen Project

## Introduction
This project is a Django project to represent a restaurant kitchen service.

## Features
- Authentication functionality for Cook/User
- Managing Cooks, Dishes, Ingredients and Dish Types directly from the website interface
- Admin panel for advanced managing

## Check it out!
[Restaurant Mate project is deployed to Render](https://restaurant-kitchen-mate-hcgj.onrender.com/)

## Getting Started
### Prerequisites
- Python 3.12.2
- Django 5.0.7
- Pillow 10.4.0

### Installation
Python 3 must be preinstalled.

  ```bash
  git clone https://github.com/dkibalenko/restaurant-mate
  cd restaurant-mate
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver
  ```

### Usage
To start the server run `python manage.py runserver`
Access the application at `http://localhost:8000/`

## Contributing
Fork the repository
Create a new branch (`git checkout -b <new_branch_name>`)
Commit your changes (`git commit -am 'message'`)
Push the branch to GitHub (`git push origin <new_branch_name>`)
Create a new Pull Request
