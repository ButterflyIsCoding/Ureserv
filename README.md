# RESERVATION Mobile App


---

## Table des Matières
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation/Deployment](#installation)
4. [Usage](#usage)
5. [Project architecture](#project architecture)
6. [License](#license)

--


## Introduction

The U-RESERVE application is designed to streamline the process of classroom reservations within the IT department from L1 to L3. This application aims to improve planning efficiency and manage classroom usage, catering primarily to students, teachers, and delegates within this department.

This document provides instructions for dockerizing and deploying the U-Reserve backend.

## General features
- Authentication : Users can register and log in based on their roles which are etudiant, administrateur, or delegue.
This process ensures secure access and role-based permissions, maintaining data integrity and user confidentiality.

- Reservation Management: Delegates can make reservations by selecting available classrooms, specifying time slots, and providing relevant information.
 The system manages these reservations and notifies professors for validation, thus ensuring structured oversight of classroom allocations.
 
- Reservation Review and Deletion: Users can view existing reservations and, depending on their roles, either cancel or delete them. This functionality allows for flexible management of bookings and helps prevent scheduling conflicts.

## Specific backend features
##auth app

   - RegisterView() : Which permit to register users.
   - LoginView() : Helps to login after registration.
   - ApproveDelegateView() : Helps to approve pending delegates.
   - PendingDelegatesView() : Obtain the list of all the pending delegates.
##Reservationapp
   - PermissionMakeReservation() : Test if the person trying to make reservation have the required priviledges.
   - ResearchDate() : Search for available halls.
   - get_available_hours() : Get available hours.
   - MakeReservation() : Helps to make a reservation.
   - ValidateReservation() : Validate reservation by the teacher using a token and through validation email.
   - GetReservationsByLevel() : Search reservations by level.
   - GetNotificationsByLevel() : Getting the notifications by level.
   - InfoReservation() : Getting all informations concerning a particular reservation.
   - PotentialReservationsToCancel() : List of reservations that can be canceled.
   - CancelReservation() : Cancel a particular reservation.
   - CancelAllReservations() : Cancel all reservations.
   - AutoDeleteExpiredReservations() : Automatically delete all reservations.
---

## Installation

    ## Prerequisit
    - **Python** (version 3.x)
    - **python3-env**
    - **Docker**
    - **Docker-compose**
    - **Django**
    - **git**
    - NB: **The SGBD used is the native django sqlite3**
    
    ##NB it is important to note that the backend is made is a DjangoRestApi backend, and therefore these APIs are written to be called and work only with the U-Reserve application. Consequently there is no website or web pages which could allow them to be tested outside of the dedicated application.
    
## Installation and deployment using docker and docker-compose.yml files
        step1 : ** Clonning the project on a local computer or a remote server on which the project will be hosted **
        
            git clone git@github.com:ButterflyIsCoding/Ureserv.git
            
        step2 : ** Moving into the directory containing the docker and docker-compose.yml files **
        
            cd ureserve_back_heil
            
        step3 : ** Building up the docker image with al the required dependancies **
        
            sudo docker-compose build
            
        step4 : ** Running the output in background so as to avoid stopping it with a ctrl+c combination or closing the command line interface **
        
            sudo docker-compose up -d 
            
        step5 : ** Testing if the backend is well fonctionning. **
            
            - open the web browser and type the URL to have access to the database : http://127.0.0.1:8000/admin
            - email : htchamba124@gmail.com
            - password : nana.heil
            
            
## Installation on local machine using python-env
        step1 : ** Clonning the project on a local computer or a remote server on which the project will be hosted **
        
            git clone git@github.com:ButterflyIsCoding/Ureserv.git
            
        step2 : ** Moving into the directory containing the docker and docker-compose.yml files **
        
            cd ureserve_back_heil
            
        step3 : ** Creating a virtual environment in which all the requirements will be installed **
            
            python3 -m venv .venv
            
        step4 : ** Connecting to the virtual environment **
            
            source .venv/bin/activate
            
        step5 : ** Installing dependencies **
        
            pip3 install -r requirements.txt
            
        step6 : ** Creating migraion files and applying them to the database**
        
            python3 manage.py makemigrations
            
            python3 manage.py migrate
            
        step7 : ** Running django integrated server **
        
            python3 manage.py runserver
            
        step8 : ** Testing if the backend is well fonctionning. **
            
            - open the web browser and type the URL to have access to the database : http://127.0.0.1:8000/admin
            - email : htchamba124@gmail.com
            - password : nana.heil

        
---
## Project Architecture

    **Architecture utiliser est une architecture MVT**

.
└── ureserve_back_heil
    ├── authapp
    │   ├── migrations
    │   │   └── __pycache__
    │   └── __pycache__
    ├── reservationapp
    │   ├── migrations
    │   │   └── __pycache__
    │   └── __pycache__
    ├── ReserveProject
    │   └── __pycache__
    ├── static
    │   ├── css
    │   └── images
    ├── staticfiles
    │   ├── admin
    │   │   ├── css
    │   │   │   └── vendor
    │   │   │       └── select2
    │   │   ├── img
    │   │   │   └── gis
    │   │   └── js
    │   │       ├── admin
    │   │       └── vendor
    │   │           ├── jquery
    │   │           ├── select2
    │   │           │   └── i18n
    │   │           └── xregexp
    │   ├── css
    │   ├── images
    │   └── rest_framework
    │       ├── css
    │       ├── docs
    │       │   ├── css
    │       │   ├── img
    │       │   └── js
    │       ├── fonts
    │       ├── img
    │       └── js
    ├── templates
    └── webfront
        ├── migrations
        │   └── __pycache__
        └── __pycache__

   ## **Root directory is ureserve_back_heil**
   ## **Principales apps :**
        - authapp
        -reservationapp

---
## Usage
1. **In the beginning**:
    You can register (as a delegate or student) or log in
   
2. **Once connected**
    - As a student:
        Check the classes scheduled and in which rooms they are scheduled
    - As a delegate:
        You can make reservations and cancel them
    - As administrateur:
        Can cancel reservations, approve pending delegates...
        
        
## The app is available via the link : https://ureserve.smartcloudservices.cloud/
 
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


