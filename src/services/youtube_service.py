from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from termcolor import colored
from config.config import CHANNEL_ID
from src.audio.transcription_manager import TranscriptionManager
import os
import pickle
from datetime import datetime, timedelta
import locale
from unidecode import unidecode

class YouTubeFetcher:
    def __init__(self, data_manager):
        try:
            print(colored("Initializing YouTube API client...", "yellow"))
            self.data_manager = data_manager
            self.transcription_manager = TranscriptionManager()
            self.scopes = ['https://www.googleapis.com/auth/youtube.readonly']
            self.credentials = None
            self.credentials_file = 'data/credentials/client-secret.json'
            self.token_file = 'data/credentials/token.pickle'
            
            # Token pickle file stores the user's credentials from previously successful logins
            if os.path.exists(self.token_file):
                print(colored("Loading cached credentials...", "yellow"))
                with open(self.token_file, 'rb') as token:
                    self.credentials = pickle.load(token)

            # If there are no valid credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    print(colored("Refreshing access token...", "yellow"))
                    self.credentials.refresh(Request())
                else:
                    print(colored("Fetching new credentials...", "yellow"))
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.scopes)
                    self.credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.token_file, 'wb') as token:
                    print(colored("Saving credentials to token.pickle...", "yellow"))
                    pickle.dump(self.credentials, token)

            self.service = build('youtube', 'v3', credentials=self.credentials)
            print(colored("✓ YouTube API client initialized", "green"))
            
        except Exception as e:
            print(colored(f"Error initializing YouTube API client: {str(e)}", "red"))
            raise

    def get_spanish_day_name(self, date):
        """
        Returns Spanish day name regardless of system locale
        """
        days = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo"
        }
        return days[date.weekday()]

    def get_spanish_month_name(self, month):
        """
        Returns Spanish month name
        """
        months = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        return months[month]

    def fetch_recent_videos(self, days=2):
        """
        Fetches all videos from the last specified days
        """
        try:
            print(colored(f"Fetching videos from the last {days} days...", "yellow"))
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            print(colored(f"Fetching videos from {start_date} to {end_date}", "yellow"))
            
            search_response = self.service.search().list(
                part="snippet,contentDetails",
                channelId=CHANNEL_ID,
                maxResults=100,
                type="video",
                order="date",
                publishedAfter=start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                publishedBefore=end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            ).execute()
            
            videos = []
            for item in search_response.get('items', []):
                print(colored(f"Found video: {item['snippet']['title']}", "cyan"))
                # Obtener el transcript del video
                transcript = self.get_video_transcript(item["id"]["videoId"])
                video = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "transcript": transcript,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "published_at": item["snippet"]["publishedAt"]
                }
                videos.append(video)
            
            if videos:
                self.data_manager.add_videos(videos)
                print(colored(f"✓ Fetched {len(videos)} videos", "green"))
                # Debug: mostrar todos los videos en caché
                self.data_manager.print_all_videos()
            return videos
            
        except HttpError as e:
            print(colored(f"YouTube API error: {str(e)}", "red"))
            raise
        except Exception as e:
            print(colored(f"Error fetching videos: {str(e)}", "red"))
            raise

    def get_video_transcript(self, video_id):
        """Get transcript for a specific video"""
        try:
            # Primero intentamos obtener el transcript de YouTube
            captions = self.service.captions().list(
                part="snippet",
                videoId=video_id
            ).execute()
            
            if captions.get('items'):
                caption_id = captions['items'][0]['id']
                transcript = self.service.captions().download(
                    id=caption_id,
                    tfmt='srt'
                ).execute()
                return transcript
            
            # Si no hay transcript en YouTube, usamos Whisper
            print(colored("No YouTube transcript available, using Whisper...", "yellow"))
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            transcript = self.transcription_manager.get_transcript(video_url)
            return transcript
            
        except Exception as e:
            print(colored(f"Error getting transcript: {str(e)}", "red"))
            return None

    def get_evangelio_video(self, target_date=None):
        """
        Gets evangelio video for a specific date
        """
        if target_date is None:
            target_date = datetime.now().date()
            print(colored(f"Looking for evangelio video for date: {target_date}", "yellow"))

        # First try to find in cache
        video = self.data_manager.find_evangelio_video(target_date)
        if video:
            print(colored("Found video in cache", "green"))
            return video

        print(colored("Video not found in cache, fetching recent videos...", "yellow"))
        # If not found, fetch recent videos and try again
        self.fetch_recent_videos(days=3)  # Aumentamos a 3 días para tener más margen
        return self.data_manager.find_evangelio_video(target_date) 