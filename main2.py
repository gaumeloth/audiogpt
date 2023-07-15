import subprocess
import sys


def richiama_tgpt(testo):
    comando = ['tgpt', f'"{testo}"']  # Comando da eseguire con il testo trascritto come input
    output = subprocess.check_output(comando)
    risposta_tgpt = output.decode('utf-8').strip()  # Converto l'output in una stringa senza spazi bianchi

    return risposta_tgpt

def formatta_risposta(stringa, stringa_da_rimuovere):
    righe = stringa.splitlines()
    righe_rimanenti = righe[2:]
    stringa_unificata = ''.join(righe_rimanenti)
    
    indice_inizio_stringa = stringa_unificata.find(stringa_da_rimuovere)
    if indice_inizio_stringa != -1:
        stringa_modificata = stringa_unificata[indice_inizio_stringa + len(stringa_da_rimuovere):]
    else:
        stringa_modificata = stringa_unificata
    return stringa_modificata

# Esempio di utilizzo
testo_domanda = sys.argv[1]
risposta_tgpt = richiama_tgpt(testo_domanda)
risposta_formattata = formatta_risposta(risposta_tgpt,testo_domanda) 
print("Risposta da tgpt:", risposta_formattata)
