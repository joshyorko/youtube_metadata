import requests
from typing import Optional
from rich import print
import logging
from rich.console import Console
from rich.traceback import install as install_traceback

install_traceback()
console = Console()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TranscribeClient:
    def __init__(self, base_url: str = "http://localhost:8007"):
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
                console.print("[green]Successfully logged in and obtained token[/green]")
                return True
            else:
                console.print(f"[red]Login failed: {response.status_code} - {response.text}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Error during login: {str(e)}[/red]")
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
                console.print("[green]Successfully transcribed video[/green]")
                # Debug print to see raw response
                console.print("\n[bold]Raw Response Data:[/bold]")
                #console.print(response.json())
                return response.json()
            else:
                console.print(f"[red]Transcription failed: {response.status_code} - {response.text}[/red]")
                return {}
                
        except Exception as e:
            console.print(f"[red]Error during transcription: {str(e)}[/red]")
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
            console.print("\n[bold]Transcription Result:[/bold]")
            console.print(result)
            # Print transcription segments
            for segment in result.get("segments", []):
                console.print(f"\n[yellow]Time: {segment['start']:.2f}s -> {segment['end']:.2f}s[/yellow]")
                console.print(f"Text: {segment['text']}")
            
            # Print transcription info
            info = result.get("info", {})
            console.print(f"\n[bold]Info:[/bold]")
            console.print(f"Language: {info.get('language', 'unknown')}")
            console.print(f"Language Probability: {info.get('language_probability', 0):.2f}")
            console.print(f"Duration: {(info.get('duration') or 0):.2f}s")

if __name__ == "__main__":
    main()