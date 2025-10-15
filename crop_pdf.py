#!/usr/bin/env python3
from PyPDF2 import PdfReader, PdfWriter
import glob
import os
import re

def extract_last_3_digits(filename):
    """Estrae le ultime 3 cifre dal nome del file"""
    base = os.path.splitext(filename)[0]
    numbers = re.findall(r'\d+', base)
    if numbers:
        last_num = numbers[-1]
        return last_num[-3:] if len(last_num) >= 3 else last_num.zfill(3)
    return None

def crop_pdf(input_file, output_file):
    """Ritaglia il PDF in base al numero finale del nome file e salva individualmente"""
    reader = PdfReader(input_file)
    writer = PdfWriter()

    final_num_str = extract_last_3_digits(os.path.basename(input_file))

    if final_num_str is None:
        print(f"⚠ Attenzione: {input_file} non ha numeri nel nome, salto il file")
        return False

    final_num = int(final_num_str)
    is_odd = final_num % 2 == 1

    for page in reader.pages:
        new_page = writer.add_page(page)

        if is_odd:
            # File con numero dispari - bordo in ALTO
            new_page.mediabox.lower_left = (35, 0)
            new_page.mediabox.upper_right = (580, 725)
        else:
            # File con numero pari - bordo in BASSO
            new_page.mediabox.lower_left = (0, 100)
            new_page.mediabox.upper_right = (520, 830)

    with open(output_file, "wb") as output:
        writer.write(output)

    print(f"✓ Processato {os.path.basename(input_file)} → {os.path.basename(output_file)} ({'dispari' if is_odd else 'pari'})")
    return True

def process_all_pdfs():
    """Processa tutti i PDF dalla directory di input alla directory di output"""
    input_dir = os.getenv("INPUT_DIR")
    output_dir = os.getenv("OUTPUT_DIR")

    if not input_dir:
        print("✗ Errore: variabile d'ambiente INPUT_DIR non impostata")
        return

    if not output_dir:
        print("✗ Errore: variabile d'ambiente OUTPUT_DIR non impostata")
        return

    if not os.path.exists(input_dir):
        print(f"✗ Errore: la directory di input '{input_dir}' non esiste")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Creata directory di output: {output_dir}")

    pdf_files = sorted(glob.glob(os.path.join(input_dir, "*.pdf")))

    if not pdf_files:
        print(f"Nessun file PDF trovato in {input_dir}")
        return

    print(f"\nTrovati {len(pdf_files)} file PDF in {input_dir}\n")

    processed = 0
    for pdf_file in pdf_files:
        try:
            last_3_digits = extract_last_3_digits(os.path.basename(pdf_file))
            if last_3_digits:
                output_filename = f"{last_3_digits}.pdf"
                output_path = os.path.join(output_dir, output_filename)

                if crop_pdf(pdf_file, output_path):
                    processed += 1
        except Exception as e:
            print(f"✗ Errore nel processare {os.path.basename(pdf_file)}: {e}")

    print(f"\n✓ Completato: {processed}/{len(pdf_files)} file processati")

if __name__ == "__main__":
    process_all_pdfs()
