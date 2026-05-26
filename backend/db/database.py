# Import MongoClient from PyMongo to connect to our MongoDB database
from pymongo import MongoClient
# Import our settings to securely access the MONGO_URI
from config.settings import settings
# Import the logging module to print messages to the console
import logging

# Set up a logger for this specific file
logger = logging.getLogger(__name__)

# Initialize collections to None
chats_collection = None
qa_collection = None

try:
    # Initialize the MongoDB client using the URI from our .env file
    client = MongoClient(settings.MONGO_URI)
    
    # Access the specific database named 'chatbot_db' (it will be created automatically if it doesn't exist)
    db = client.chatbot_db
    
    # Access the 'chats' collection to store overall chat sessions
    chats_collection = db["chats"]
    # Access the 'qa_pairs' collection to store individual questions and answers
    qa_collection = db["qa_pairs"]
    
    # Log a success message if the connection works
    logger.info("Connected to MongoDB successfully.")
except Exception as e:
    # Log an error message if the connection fails
    logger.error(f"Could not connect to MongoDB: {e}")
