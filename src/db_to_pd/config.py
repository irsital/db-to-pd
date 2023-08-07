""" Handles loading the configuration from a dotenv file. """
from pathlib import Path
import os
from dotenv import load_dotenv


def load_config() -> dict:
    """
    Loads the .env file and returns its contents as a dictionary.

    Returns:
        A dictionary containing the contents of the .env file.
    """
    env_file_path = os.getenv('ENV_FILE_PATH', '.env')
    env_file_path = Path(env_file_path).resolve()

    if env_file_path.exists():
        load_dotenv(dotenv_path=env_file_path)

    config = {
        'database': {
            'host': os.getenv('DATABASE_HOST'),
            'port': int(os.getenv('DATABASE_PORT')),
            'name': os.getenv('DATABASE_NAME'),
            'schema': os.getenv('DATABASE_SCHEMA'),
            'user': os.getenv('DATABASE_USER'),
            'password': os.getenv('DATABASE_PASSWORD'),
        },
        'ssh': {
            'host': os.getenv('SSH_HOST'),
            'port': int(os.getenv('SSH_PORT')),
            'username': os.getenv('SSH_USERNAME'),
            'password': os.getenv('SSH_PASSWORD'),
        }
    }

    return config
