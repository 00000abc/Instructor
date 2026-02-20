#!/usr/bin/env bash
# Script de build pour Render
# exit on error
set -o errexit 

# Installer les dépendances
pip install -r /upload-backend/monprojet/requirements.txt

# Collecter les fichiers statiques
python /upload-backend/monprojet/manage.py collectstatic --no-input

# Faire les migrations
python /upload-backend/monprojet/manage.py migrate
