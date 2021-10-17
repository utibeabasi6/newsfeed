import random
from dotenv import load_dotenv
import os
from pathlib import Path


def generate_secret_key():
    """
    Generates and returns a unique secret key to be used in our application
    :return: String
    """
    letters = [chr(random.randint(65, 122)) for i in range(10)]
    return ''.join(letters)


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Sets up configuration from .env file and initializes a secret key
    """
    # Loading the environment variables

    HOST = os.getenv('SERVER')
    SECRET_KEY = generate_secret_key()
    TESTING = os.getenv('TESTING')
    DEBUG = os.getenv('DEBUG')
    API_KEY = os.getenv('API_KEY')
