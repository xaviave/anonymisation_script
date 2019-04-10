# Anonymisation Project

## Introduction

> This project provide a tool to anonymize some dumped data from SQL file to make sure that those data are protected and the society follow the RGPD law

## Installation

> Clone the repository and chose what you need :

- an anonymisation script for people who like their bash and wanted to write a command line.
  To run it, simply go to "script_anonymisation/" and then run this command line :
    > python3 anonymize.py [ file_to_anonymize ] [ table:parameter ]

- the graphical version where your mouse is needed.
  To run it, go to "app_anonymize/", make sure your localhost:8000 is free and then run:
    > python 3 manage.py runserver
   Just go on the app on localhost:8000 and enjoy anonymize some datas!
