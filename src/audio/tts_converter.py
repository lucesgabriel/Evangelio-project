from gtts import gTTS
from termcolor import colored
import os
from openai import OpenAI
from pathlib import Path
from config.config import OPENAI_API_KEY

class TTSConverter:
    def __init__(self):
        self.output_dir = "audio_files"
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.VOICE_MODEL = "tts-1-hd"  # Using HD model for better quality
        self.VOICE_NAME = "onyx"  # Male voice with Latino accent
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        except Exception as e:
            print(colored(f"Error creating output directory: {str(e)}", "red"))
            raise

    def convert_text_to_audio(self, text, evangelio_only=False):
        """
        Converts text to audio using OpenAI's TTS API
        """
        try:
            print(colored("Converting text to audio...", "yellow"))
            
            # Si solo queremos el evangelio, extraemos esa parte
            if evangelio_only:
                text = self.extract_evangelio_text(text)
            
            output_file = "evangelio.mp3"
            
            try:
                # Intentar usar OpenAI TTS primero
                print(colored(f"Using OpenAI TTS with {self.VOICE_NAME} voice...", "yellow"))
                response = self.client.audio.speech.create(
                    model=self.VOICE_MODEL,
                    voice=self.VOICE_NAME,
                    input=text
                )
                
                # Save the audio file
                response.stream_to_file(output_file)
                print(colored("✓ Audio conversion successful with OpenAI TTS", "green"))
            except Exception as e:
                print(colored(f"Error with OpenAI TTS: {str(e)}", "red"))
                print(colored("Falling back to gTTS...", "yellow"))
                # Fallback to gTTS if OpenAI fails
                tts = gTTS(text=text, lang='es', slow=False)
                tts.save(output_file)
                print(colored("✓ Audio conversion successful with gTTS fallback", "green"))
            
            return output_file
        except Exception as e:
            print(colored(f"Error converting text to audio: {str(e)}", "red"))
            raise

    def extract_evangelio_text(self, full_text):
        """Extrae solo la parte del evangelio del texto completo"""
        try:
            # Buscar el inicio del evangelio
            start_marker = "Del Santo Evangelio según"
            end_markers = ["Palabra del Señor", "Palabra de Dios"]
            
            start_idx = full_text.find(start_marker)
            if start_idx == -1:
                return full_text
            
            # Encontrar el final del evangelio
            text = full_text[start_idx:]
            end_idx = -1
            
            for marker in end_markers:
                temp_idx = text.find(marker)
                if temp_idx != -1:
                    end_idx = temp_idx
                    break
            
            if end_idx != -1:
                # Extraer el texto hasta el marcador de fin
                text = text[:end_idx].strip()
            
            # Limpiar formato
            text = text.replace("*", "").strip()
            
            # Agregar las frases finales
            text = f"{text}\n\nPalabra del Señor.\nGloria a ti Señor Jesús."
            
            return text
        except Exception as e:
            print(colored(f"Error extracting evangelio text: {str(e)}", "red"))
            return full_text 