# Challenge-Memorize
### [Challenge-Memorize](https://keinermendoza.com/demonstration-projects/memorize/) is the web app where you memorize whatever you want with fun. 

You can [try the app online here](https://keinermendoza.com/demonstration-projects/memorize/) or clone this repo if you want.

## Quick Start

Create and activate a virtual enviorment

```shell
python3 -m venv venv
source venv/bin/activate
```
Install the development dependencies
```shell
pip3 install -r requirements_development.txt
```

Now you can create your database with the command
```shell
python3 manage.py migrate
```

finally you can spin up the development server with

```shell
python3 manage.py runserver
```
If you want to modify the tailwindcss classes you can install it running
```shell
npm i
```
and running in a separate console the command
```shell
npm run tailwind
```
That's all!
## Some features

🏭 Dinamic Content Generetion (using Django)

📱 💻 Responsive Design

🧑‍🤝‍🧑 Accounts 

⬆️ Upload Data in administration site via CSV

🎮 Interactive User Interface

## The stack I used 

✔️ Django

✔️ HTMX

✔️ Tailwindcss

✔️ Javascript

✔️ CSS (for some animations)

## Some of the tasks I did to get it ready

✔️ Design the user interface

✔️ Write Content

✔️ Create models for the database

✔️ Create and handel database constraints

✔️ Create validations in form and views for data

✔️ Manage Actualization of User Interface

✔️ Rent a Virtual Machine

✔️ Buy the Domain

✔️ Configure the SSL Certificate

✔️ Configure Nginx Servers + Nginx as Reverse Proxy + WSGI

## For Django Readers

If you like Django, you may find interesting some particular pieces of code. You can take a look at the custom_login_required decorator that extends the functionality of the Django login_required, or the CustomModelAdmin class that allows the upload of data via CSV.

I had a lot of fun writing this app, and also learned some interesting things. I hope you like it almost as much as I do. Feel free to do whatever you want with the code.
