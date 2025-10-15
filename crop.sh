#!/bin/bash

# Controlla se la cartella venv esiste già
if [ ! -d "./py_pdf" ]; then
    echo "Creazione venv..."
    python3 -m venv ./py_pdf
    source ./py_pdf/bin/activate
    echo "Installazione PyPDF2..."
    python3 -m pip install PyPDF2
else
    echo "Venv già esistente, attivazione..."
    source ./py_pdf/bin/activate
fi

# Esegui lo script
python3 ./crop_pdf.py

# Deattiva il venv (opzionale)
deactivate