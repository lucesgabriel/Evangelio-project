from termcolor import colored
import sys

# Servicios
from src.services.youtube_service import YouTubeFetcher
from src.services.gemini_service import GeminiAPI
from src.services.whatsapp_service import WhatsAppSender

# Audio
from src.audio.tts_converter import TTSConverter

# Datos
from src.data.data_manager import DataManager

# Configuración
from config.config import WHATSAPP_RECIPIENT

def main():
    try:
        print(colored("Starting evangelio service...", "blue"))
        
        # Initialize services
        data_manager = DataManager()
        youtube = YouTubeFetcher(data_manager)
        gemini = GeminiAPI()
        tts = TTSConverter()
        whatsapp = WhatsAppSender()

        # Fetch video
        video_info = youtube.get_evangelio_video()
        if not video_info:
            print(colored("No evangelio video found for today", "yellow"))
            sys.exit(1)

        # Extract evangelio text from transcript using Gemini
        if video_info.get('transcript'):
            print(colored("\n=== Original Transcript ===", "blue"))
            print(colored(video_info['transcript'], "white"))
            print(colored("========================", "blue"))
            
            prompt = f"""
            Por favor, analiza el siguiente transcript del video y:
            1. Identifica y extrae el texto del evangelio (la lectura bíblica)
            2. Ignora introducciones, comentarios y reflexiones personales
            3. Formatea el texto en párrafos claros
            4. Incluye la referencia bíblica si está disponible
            
            {video_info['transcript']}
            """
        else:
            # Si no hay transcript, usamos la descripción
            print(colored("\n=== No transcript available, attempting to download and transcribe video ===", "yellow"))
            try:
                video_url = f"https://www.youtube.com/watch?v={video_info['video_id']}"
                transcript = youtube.transcription_manager.get_transcript(video_url)
                if transcript:
                    print(colored("\n=== Whisper Transcript ===", "blue"))
                    print(colored(transcript, "white"))
                    print(colored("========================", "blue"))
                    prompt = f"""
                    Por favor, analiza el siguiente transcript del video y:
                    1. Identifica y extrae el texto del evangelio (la lectura bíblica)
                    2. Ignora introducciones, comentarios y reflexiones personales
                    3. Formatea el texto en párrafos claros
                    4. Incluye la referencia bíblica si está disponible
                    
                    {transcript}
                    """
                else:
                    print(colored("\n=== Using video description as fallback ===", "yellow"))
                    prompt = f"Resume brevemente el siguiente evangelio: {video_info['description']}"
            except Exception as e:
                print(colored(f"\nError transcribing video: {str(e)}", "red"))
                prompt = f"Resume brevemente el siguiente evangelio: {video_info['description']}"

        # Generate summary with Gemini
        summary = gemini.generate_text(prompt)
        print(colored("\n=== Processed Evangelio Text ===", "green"))
        print(colored(summary, "white"))
        print(colored("============================", "green"))

        # Prepare full text
        evangelio_text = f"{video_info['title']}\n\nEvangelio:\n{summary}"

        # Convert to audio
        audio_file = tts.convert_text_to_audio(evangelio_text, evangelio_only=True)

        # Send to WhatsApp
        print(colored(f"Sending message to {WHATSAPP_RECIPIENT}...", "yellow"))
        whatsapp.send_message(WHATSAPP_RECIPIENT, evangelio_text)
        whatsapp.send_audio(WHATSAPP_RECIPIENT, audio_file, "Evangelio del día")

        print(colored("✓ Process completed successfully", "green"))

    except Exception as e:
        print(colored(f"Error in main process: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 