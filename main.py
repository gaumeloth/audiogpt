import sounddevice as sd
import numpy as np
import keyboard
import speech_recognition as sr
import soundfile as sf
import subprocess

def registra_audio():
    fs = 44100  # Frequenza di campionamento
    registrazione = []
    
    def callback(indata, frames, time, status):
        registrazione.append(indata.copy())

    stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    stream.start()
    
    print("Registrazione in corso... Premi invio per interrompere.")
    keyboard.wait('enter')  # Attendiamo la pressione del tasto Enter per interrompere la registrazione
    
    stream.stop()
    stream.close()
    
    audio_registrato = np.concatenate(registrazione)
    print("Registrazione terminata")

    # Salviamo l'audio su un file temporaneo
    audio_file_temporaneo = "audio_temp.wav"
    sf.write(audio_file_temporaneo, audio_registrato, fs)
    
    return audio_file_temporaneo

def trascrivi_audio(audio_file_temporaneo):
    recognizer = sr.Recognizer()
    
    # Trascrizione dell'audio
    testo_trascritto = ""

    with sr.AudioFile(audio_file_temporaneo) as source:
        audio = recognizer.record(source)  # Caricamento dell'audio

        try:
            testo_trascritto = recognizer.recognize_google(audio, language="it-IT")
        except sr.UnknownValueError:
            print("Impossibile trascrivere l'audio. Audio non riconosciuto.")
        except sr.RequestError as e:
            print(f"Impossibile completare la richiesta al servizio di riconoscimento vocale: {e}")

    return testo_trascritto

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

def main():
    audio_registrato = registra_audio()
    testo_trascritto = trascrivi_audio(audio_registrato)
    print("Domanda capita:", testo_trascritto)
    risposta_tgpt = richiama_tgpt(testo_trascritto)
    risposta_formattata = formatta_risposta(risposta_tgpt, testo_trascritto) 
    print("Risposta da tgpt:", risposta_formattata)

if __name__ == "__main__":
    main()
