#!/usr/bin/env bash
# Script de build pour Render
# exit on error
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --no-input

# Faire les migrations
python manage.py migrate