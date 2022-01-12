#!/bin/bash

echo "Download latest version of main.py from cloud storage"
gsutil -o Credentials:gs_service_key_file=secret/apes-313514-90a1ec369f58.json cp gs://academia-assistant/backend-vm/main.py /app/main.py

echo "starting webserver"
FILE=/app/main.py
if [ -f "$FILE" ]; then
    gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
else 
    echo "$FILE does not exist."
fi