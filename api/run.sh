#!/bin/bash
# Levanta la API de Reporter IA Atom en http://localhost:8000
# Uso: bash run.sh

cd "$(dirname "$0")"

# Credenciales BigQuery
export GOOGLE_APPLICATION_CREDENTIALS="/Users/pedrokopyto/.config/gcloud/atom-brain-key.json"

# Instalar dependencias si no están
pip3 install -r requirements.txt -q

# Levantar servidor
python3 -m uvicorn main:app --reload --port 8000
