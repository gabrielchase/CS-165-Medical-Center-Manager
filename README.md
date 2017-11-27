# Medical Center Manager
Our system will allow patients to create accounts in order to view the information of each institution such as the services, contact numbers, and others. The user may search for the institution nearest to his/her location and can set an appointment on a specific service offered by the chosen institution. After visiting the institution, the user may also give their feedback and rating on the institution or service. Each institution is handled by an administrator, a member of the staff, who can add, update, or delete the institution’s information and also manage the appointments made. Each institution will also have a database of BFA-accredited products and drugs, showing the function and price, that can be viewed and searched by the regular users and these information will be handled by the administrator.

### Members:
  - Treacy Evangelista
  - Mikayla Lopez
  - Gabriel Patron
  - Juan Gabriel Tamayo
  
### Installation and Set Up

This project's main dependencies are Python 3, pip3, a virtualenv, Django 1.11, and MySQL.
I will cover installation of pip, virtualenvs, Django and how to set up the project. I will not cover MySQL installations. I use a Mac so I'm not 100% sure about Linux installations.

### Installing Python3 and Pip3
On Linux

    $ sudo apt-get update
    $ sudo apt-get install python3.6
    $ sudo apt-get -y install python3-pip
    
On Mac
    
    $ brew install python3
    $ brew postinstall python3
    
To check if it works **_python3_** should open up the python shell and **_pip3_** should display all the commands and flags for pip.

### Installing virtualenvs
What is a virtualenv?
> virtualenv is a tool to create isolated Python environments. virtualenv  creates a folder which contains all the necessary executables to use the          packages that a Python project would need.

    $ pip3 install virtualenv
    
Test installation
    
    $ virtualenv --version
    
### Create the database
Open your MySQL client and type: **CREATE DATABASE medcentermanager_db;**

### Cloning the Project
1. Go to the directory where you want to clone the project
2. Create your virtualenv. I have my envname as the project name _'medcentermanager'_
    > $ virtualenv -p python3 envname
3. 
    > $ virtualenv -p python3 envname
4. **cd inside your virutalenv**. You should see the following folders inside the virtualenv: _bin_, _include_, _lib_ inside
    > $ cd envname
5. Activate the virtualenv. You should see _(envname)_ before your terminal name after typing the following command.
    > $ source bin/activate
6. Clone the repository
    > $ git clone https://github.com/gabrielchase/CS-165-Medical-Center-Manager.git
7. Install the project requirements
    > $ pip3 install -r requirements.txt
8. cd into the folder project and check for the folder with the file 'manage.py'
9. Make database migrations
    > $ python manage.py makemigrations
10. Migrate the database
    > $ python manage.py migrate
11. Test to see if it's working. (4 tests should pass)
    > $ python manage.py test users.tests
12. Run the server with:
    > $ python manage.py runserver
13. Install NodeJS + NPM: https://docs.npmjs.com/getting-started/installing-node
14. Install bower: https://bower.io/
15. Install bower components in your project
    > $ python manage.py bower install


### Endpoints

#### Registration

Register as a regular user

    '/registration/regular'

Register as an institution administrator

    '/registration/administrator'

After registration you should be sent to the log in screen

#### Login

Login using the registered user's email at 

    '/login'

This should take you to the dashboard


#### Dashboard

As of now (Nov 7), you can see a logout and edit my profile buttons at the top

    '/dashboard'

Edit my profile brings you to the following link where you may update your details

    '/users/edit'

Logout will log you out lol

    '/logout'

#### Insitutions

While logged in you may visit the following link to do a search:

    '/dashboard/search

You may query by changing the url parameters, *'l'* for location and *'c'* for category.
Of course you have to populate the database first with administrator accounts.

    '/dashboard/search?c=treatment_center'
    '/dashboard/search?l=Makati'
    '/dashboard/search?c=testing_hub&l=quezon%20city'
    