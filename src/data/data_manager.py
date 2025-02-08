import json
import pandas as pd
from datetime import datetime, timedelta
from termcolor import colored
import os

class DataManager:
    def __init__(self):
        self.cache_file = 'data/cache/videos_cache.json'
        self.df = None
        self.columns = [
            'video_id', 'title', 'description', 'url', 
            'published_at', 'fetch_date', 'transcript'
        ]
        self.load_cache()

    def load_cache(self):
        """Load cached videos from JSON file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.df = pd.DataFrame(data)
                print(colored("✓ Cache loaded successfully", "green"))
            else:
                self.df = pd.DataFrame(columns=self.columns)
                print(colored("Created new cache", "yellow"))
        except Exception as e:
            print(colored(f"Error loading cache: {str(e)}", "red"))
            self.df = pd.DataFrame(columns=self.columns)

    def save_cache(self):
        """Save videos to JSON cache file"""
        try:
            self.df.to_json(self.cache_file, orient='records', force_ascii=False)
            print(colored("✓ Cache saved successfully", "green"))
        except Exception as e:
            print(colored(f"Error saving cache: {str(e)}", "red"))

    def add_videos(self, videos):
        """Add new videos to the dataframe"""
        try:
            new_df = pd.DataFrame(videos)
            new_df['fetch_date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.df.drop_duplicates(subset=['video_id'], keep='last', inplace=True)
            self.save_cache()
        except Exception as e:
            print(colored(f"Error adding videos: {str(e)}", "red"))

    def find_evangelio_video(self, target_date):
        """Find evangelio video for specific date"""
        try:
            # Convert target_date to string for comparison
            target_date_str = target_date.strftime('%Y-%m-%d')
            print(colored(f"Searching for video with date: {target_date_str}", "yellow"))
            
            # Primero intentamos buscar por fecha exacta en el título
            mask = (
                self.df['title'].str.contains('Evangelio', case=False, na=False) &
                self.df['title'].str.contains(str(target_date.day), na=False) &
                self.df['title'].str.contains(str(target_date.year), na=False)
            )
            
            matching_videos = self.df[mask]
            
            # Debug: mostrar los videos encontrados
            if not matching_videos.empty:
                print(colored("Found matching videos:", "cyan"))
                for _, video in matching_videos.iterrows():
                    print(colored(f"- {video['title']}", "cyan"))
            
            if not matching_videos.empty:
                # Ordenar por fecha de publicación (más reciente primero)
                matching_videos = matching_videos.sort_values('published_at', ascending=False)
                video = matching_videos.iloc[0]
                print(colored(f"Selected video: {video['title']}", "green"))
                return {
                    "video_id": video['video_id'],
                    "title": video['title'],
                    "description": video['description'],
                    "url": video['url'],
                    "published_at": video['published_at']
                }
            else:
                print(colored("No matching videos found in cache", "yellow"))
            return None
        except Exception as e:
            print(colored(f"Error finding video: {str(e)}", "red"))
            return None

    def print_all_videos(self):
        """Debug method to print all videos in cache"""
        try:
            print(colored("\nAll videos in cache:", "cyan"))
            for _, video in self.df.iterrows():
                print(colored(f"\n- Title: {video['title']}", "cyan"))
                print(colored(f"  Published: {video['published_at']}", "cyan"))
                if video.get('transcript'):
                    print(colored("  [Has transcript]", "green"))
                else:
                    print(colored("  [No transcript]", "yellow"))
        except Exception as e:
            print(colored(f"Error printing videos: {str(e)}", "red")) 