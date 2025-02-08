from whatsapp_api_client_python import API
from termcolor import colored
from config.config import WHATSAPP_ID_INSTANCE, WHATSAPP_API_TOKEN

class WhatsAppSender:
    def __init__(self):
        try:
            print(colored("Initializing WhatsApp client...", "yellow"))
            self.client = API.GreenAPI(WHATSAPP_ID_INSTANCE, WHATSAPP_API_TOKEN)
            print(colored("✓ WhatsApp client initialized", "green"))
        except Exception as e:
            print(colored(f"Error initializing WhatsApp client: {str(e)}", "red"))
            raise

    def send_message(self, number, message):
        """
        Sends a text message via WhatsApp
        """
        try:
            print(colored("Sending WhatsApp message...", "yellow"))
            response = self.client.sending.sendMessage(number, message)
            print(colored("✓ Message sent successfully", "green"))
            return response
        except Exception as e:
            print(colored(f"Error sending message: {str(e)}", "red"))
            raise

    def send_audio(self, number, audio_path, caption=""):
        """
        Sends an audio file via WhatsApp
        """
        try:
            print(colored("Sending audio file...", "yellow"))
            # Get the file name from the path
            file_name = audio_path.split('/')[-1]
            response = self.client.sending.sendFileByUpload(
                chatId=number,
                path=audio_path,
                fileName=file_name,
                caption=caption
            )
            print(colored("✓ Audio file sent successfully", "green"))
            return response
        except Exception as e:
            print(colored(f"Error sending audio: {str(e)}", "red"))
            raise 