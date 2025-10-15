#!/usr/bin/env python3
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject
import glob
import os
import re

def extract_page_number(filename):
    """Estrae il numero di pagina dal nome del file (l'ultimo numero)"""
    base = os.path.splitext(filename)[0]
    numbers = re.findall(r'\d+', base)
    if numbers:
        return int(numbers[-1])
    return None

def crop_pdf_by_filename(input_file, writer):
    """Ritaglia il PDF in base al numero finale del nome file e aggiunge al writer"""
    reader = PdfReader(input_file)
    
    final_num = extract_page_number(os.path.basename(input_file))
    
    if final_num is None:
        print(f"⚠ Attenzione: {input_file} non ha numeri nel nome, salto il file")
        return 0
    
    is_odd = final_num % 2 == 1
    pages_added = 0
    
    for page in reader.pages:
        # Crea una COPIA della pagina
        new_page = writer.add_page(page)
        
        if is_odd:
            # File con numero dispari - bordo in ALTO
            new_page.mediabox.lower_left = (35, 0)
            new_page.mediabox.upper_right = (580, 725)
        else:
            # File con numero pari - bordo in BASSO
            new_page.mediabox.lower_left = (0, 100)
            new_page.mediabox.upper_right = (520, 830)
        
        pages_added += 1
    
    print(f"✓ Processato {input_file} ({'dispari' if is_odd else 'pari'}) - {pages_added} pagine")
    return pages_added

def merge_all_pdfs():
    """Unisce tutti i PDF nella cartella corrente"""
    pdf_files = sorted(glob.glob("*.pdf"))
    
    if not pdf_files:
        print("Nessun file PDF trovato nella cartella corrente")
        return
    
    # Estrai i numeri di pagina per determinare il nome del file output
    page_numbers = []
    for pdf_file in pdf_files:
        page_num = extract_page_number(pdf_file)
        if page_num is not None:
            page_numbers.append(page_num)
    
    if not page_numbers:
        print("Nessun file con numeri di pagina trovato")
        return
    
    first_page = min(page_numbers)
    last_page = max(page_numbers)
    output_filename = f"{first_page}-{last_page}.pdf"
    
    # Rimuovi il file di output se esiste nella lista
    if output_filename in pdf_files:
        pdf_files.remove(output_filename)
    
    print(f"\nTrovati {len(pdf_files)} file PDF:")
    for f in pdf_files:
        print(f"  - {f}")
    print(f"\nFile output: {output_filename}")
    print()
    
    writer = PdfWriter()
    total_pages = 0
    
    for pdf_file in pdf_files:
        try:
            pages_added = crop_pdf_by_filename(pdf_file, writer)
            total_pages += pages_added
        except Exception as e:
            print(f"✗ Errore nel processare {pdf_file}: {e}")
            import traceback
            traceback.print_exc()
    
    if total_pages > 0:
        with open(output_filename, "wb") as output:
            writer.write(output)
        print(f"\n✓ PDF finale salvato: {output_filename}")
        print(f"  Totale pagine: {total_pages}")
    else:
        print("\nNessuna pagina da salvare")

if __name__ == "__main__":
    merge_all_pdfs()
