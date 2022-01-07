## Installation

Les étapes d'installation avec Venv....

Pour Windows :
   dans l'invite de commande : ``python -m venv env``  ``env/Scripts/activate``  ``pip install -r requirements.txt``   

Pour linux :
   dans le terminal : ``sudo py3 -m venv env``  ``source env/bin/activate``  ``pip3 install -r requirements.txt``

## Démarrage

Dans un terminal :
``python manage.py runserver``

Info : le fichier de base de donnée "db.sqlite3" est fournis, aucune migration n'est necessaire, pour l'effacer :

``python manage.py flush``
