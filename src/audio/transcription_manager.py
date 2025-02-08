import os
import yt_dlp
import subprocess
import time
from termcolor import colored
from openai import OpenAI
from config.config import OPENAI_API_KEY

class TranscriptionManager:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.audio_dir = 'audio_files'
        os.makedirs(self.audio_dir, exist_ok=True)
        self.timeout = 120  # Reducido a 2 minutos por operación
        self.max_segment_size = 25 * 1024 * 1024  # 25MB máximo por segmento

    def download_audio(self, video_url):
        """Descarga el audio del video"""
        try:
            print(colored("Downloading audio...", "yellow"))
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',  # Reducida la calidad para archivos más pequeños
                }],
                'outtmpl': os.path.join(self.audio_dir, '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(colored("Extracting video info...", "yellow"))
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                audio_filename = filename.rsplit('.', 1)[0] + '.mp3'
                print(colored(f"Audio saved as: {audio_filename}", "cyan"))
                print(colored("✓ Audio downloaded successfully", "green"))
                return audio_filename
        except Exception as e:
            print(colored(f"Error downloading audio: {str(e)}", "red"))
            raise

    def split_audio(self, audio_filename, segment_length=120):  # Reducido a 2 minutos por segmento
        """Divide el audio en segmentos más pequeños"""
        try:
            print(colored("Splitting audio into segments...", "yellow"))
            print(colored(f"Analyzing audio duration...", "cyan"))
            
            # Verificar que el archivo existe
            if not os.path.exists(audio_filename):
                raise FileNotFoundError(f"Audio file not found: {audio_filename}")
            
            # Obtener duración del audio
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                text=True,
                check=True
            )
            
            total_duration = float(result.stdout)
            print(colored(f"Total audio duration: {total_duration:.2f} seconds", "cyan"))
            
            # Calcular número de segmentos
            num_segments = int(total_duration / segment_length) + 1
            print(colored(f"Will create {num_segments} segments", "cyan"))
            
            segments = []
            for i in range(num_segments):
                segment_filename = f'{audio_filename}_part{i}.mp3'
                start_time = i * segment_length
                
                print(colored(f"Processing segment {i+1}/{num_segments} (Start time: {start_time}s)...", "yellow"))
                
                try:
                    # Comando FFmpeg con opciones optimizadas
                    cmd = [
                        'ffmpeg', '-y',  # Sobrescribir archivos existentes
                        '-i', audio_filename,
                        '-ss', str(start_time),
                        '-t', str(segment_length),
                        '-acodec', 'libmp3lame',
                        '-ar', '16000',  # Reducir sample rate
                        '-ac', '1',      # Mono audio
                        '-b:a', '32k',   # Bitrate más bajo
                        segment_filename
                    ]
                    
                    # Ejecutar FFmpeg con timeout
                    process = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=60,  # 1 minuto máximo por segmento
                        check=True
                    )
                    
                    # Verificar tamaño del archivo
                    if os.path.exists(segment_filename):
                        size = os.path.getsize(segment_filename)
                        if size > 0 and size < self.max_segment_size:
                            segments.append(segment_filename)
                            print(colored(f"✓ Segment {i+1} created successfully ({size/1024/1024:.2f}MB)", "green"))
                        else:
                            raise Exception(f"Invalid segment size: {size/1024/1024:.2f}MB")
                    
                except subprocess.TimeoutExpired as e:
                    print(colored(f"Timeout processing segment {i+1}, retrying with smaller duration...", "yellow"))
                    # Intentar de nuevo con un segmento más pequeño
                    try:
                        cmd[6] = str(segment_length/2)  # Reducir duración a la mitad
                        subprocess.run(cmd, timeout=30, check=True)
                        if os.path.exists(segment_filename) and os.path.getsize(segment_filename) > 0:
                            segments.append(segment_filename)
                    except:
                        print(colored(f"Failed to process segment {i+1} even with smaller duration", "red"))
                
                except Exception as e:
                    print(colored(f"Error processing segment {i+1}: {str(e)}", "red"))
                    if os.path.exists(segment_filename):
                        os.remove(segment_filename)
            
            if not segments:
                raise Exception("No segments were created successfully")
            
            print(colored(f"✓ Audio split into {len(segments)} segments", "green"))
            return segments
            
        except Exception as e:
            print(colored(f"Error splitting audio: {str(e)}", "red"))
            # Limpiar archivos temporales en caso de error
            self.cleanup_temp_files(audio_filename)
            raise

    def cleanup_temp_files(self, base_filename):
        """Limpia archivos temporales"""
        try:
            for file in os.listdir(self.audio_dir):
                if file.startswith(os.path.basename(base_filename)):
                    try:
                        os.remove(os.path.join(self.audio_dir, file))
                    except:
                        pass
        except Exception as e:
            print(colored(f"Error cleaning up temporary files: {str(e)}", "red"))

    def transcribe_audio(self, audio_filename):
        """Transcribe el audio usando Whisper"""
        try:
            print(colored("Starting transcription...", "yellow"))
            segments = self.split_audio(audio_filename)
            full_transcript = []
            
            for i, segment in enumerate(segments, 1):
                print(colored(f"Transcribing segment {i}/{len(segments)}...", "yellow"))
                try:
                    with open(segment, 'rb') as audio_file:
                        transcript = self.client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            language="es"
                        )
                        full_transcript.append(transcript.text)
                    print(colored(f"✓ Segment {i} transcribed", "green"))
                except Exception as e:
                    print(colored(f"Error transcribing segment {i}: {str(e)}", "red"))
                finally:
                    # Limpiar segmento actual
                    if os.path.exists(segment):
                        os.remove(segment)
            
            # Limpiar archivo original
            if os.path.exists(audio_filename):
                os.remove(audio_filename)
            
            if not full_transcript:
                raise Exception("No segments were transcribed successfully")
            
            print(colored("✓ Transcription completed", "green"))
            print(colored("\nTranscript preview:", "cyan"))
            preview = ' '.join(full_transcript)[:200] + "..."
            print(colored(preview, "white"))
            return ' '.join(full_transcript)
            
        except Exception as e:
            print(colored(f"Error transcribing audio: {str(e)}", "red"))
            self.cleanup_temp_files(audio_filename)
            raise

    def get_transcript(self, video_url):
        """Obtiene la transcripción completa del video"""
        try:
            audio_filename = self.download_audio(video_url)
            transcript = self.transcribe_audio(audio_filename)
            return transcript
        except Exception as e:
            print(colored(f"Error getting transcript: {str(e)}", "red"))
            raise 