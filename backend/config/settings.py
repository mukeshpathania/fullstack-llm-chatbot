# Import load_dotenv to load environment variables from the .env file
from dotenv import load_dotenv
# Import os to access the environment variables from the operating system
import os
from pathlib import Path

# Load the .env file from the backend folder no matter where the app is started.
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env", override=True)

# Create a class to store and manage our configuration settings
class Settings:
    # Read the GROQ API key from the environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Read the MongoDB connection string from the environment variables
    MONGO_URI = os.getenv("MONGO_URI")

# Create a global instance of Settings that other files can import and use
settings = Settings()
