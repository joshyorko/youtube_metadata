import requests
from typing import Optional
from rich import print
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TranscribeClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        """Login to get JWT token"""
        login_url = f"{self.base_url}/auth/token"
        
        try:
            # Auth endpoint expects form data
            response = requests.post(
                login_url,
                data={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                print("[green]Successfully logged in and obtained token[/green]")
                return True
            else:
                print(f"[red]Login failed: {response.status_code} - {response.text}[/red]")
                return False
                
        except Exception as e:
            print(f"[red]Error during login: {str(e)}[/red]")
            return False

    def transcribe_video(self, youtube_url: str) -> dict:
        """Transcribe a YouTube video using the service"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first")

        transcribe_url = f"{self.base_url}/transcribe/"
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.post(
                transcribe_url + f"?youtube_url={youtube_url}",
                headers=headers
            )
            
            if response.status_code == 200:
                print("[green]Successfully transcribed video[/green]")
                # Debug print to see raw response
                print("\n[bold]Raw Response Data:[/bold]")
                print(response.json())
                return response.json()
            else:
                print(f"[red]Transcription failed: {response.status_code} - {response.text}[/red]")
                return {}
                
        except Exception as e:
            print(f"[red]Error during transcription: {str(e)}[/red]")
            return {}

def main():
    # Initialize client
    client = TranscribeClient()
    
    # Login credentials (using the test account from the codebase)
    username = "johndoe"
    password = "secret"
    
    # Sample YouTube URL to transcribe
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Login and transcribe
    if client.login(username, password):
        result = client.transcribe_video(youtube_url)
        
        if result:
            print("\n[bold]Transcription Result:[/bold]")
            
            # Print transcription segments
            for segment in result.get("segments", []):
                print(f"\n[yellow]Time: {segment['start']:.2f}s -> {segment['end']:.2f}s[/yellow]")
                print(f"Text: {segment['text']}")
            
            # Print transcription info
            info = result.get("info", {})
            print(f"\n[bold]Info:[/bold]")
            print(f"Language: {info.get('language', 'unknown')}")
            print(f"Language Probability: {info.get('language_probability', 0):.2f}")
            print(f"Duration: {(info.get('duration') or 0):.2f}s")

if __name__ == "__main__":
    main()