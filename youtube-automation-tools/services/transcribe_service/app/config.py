from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


def read_secret(secret_name: str) -> str:
    """
    Reads a secret from a file located at /etc/secrets/{secret_name}.

    Args:
        secret_name (str): The name of the secret file to read.

    Returns:
        str: The contents of the secret file, with leading/trailing whitespace removed.
    """
    try:
        with open(f'/etc/secrets/{secret_name}', 'r', encoding='utf-8') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return None


class Settings(BaseSettings):
    """ Describes app-wide configuration variables and environmental ones. """

    app_name: str = "Transcribe Service"

    
    environment: str = read_secret("ENVIRONMENT")
    
    secret_key: str = read_secret("SECRET_KEY")
    access_token_expire_minutes: int = int(read_secret("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

    
    #NOTE: It might be needed where you have to include the paramater env_file=".env" into the SettingsConfigDict object
    model_config = SettingsConfigDict(env_file=".env")


try:
    settings = Settings()
except ValidationError as e:
    print("Error loading settings from environment variables:", e.json())
    exit(1)
