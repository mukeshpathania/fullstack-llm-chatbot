# Import the collections we initialized in database.py
from db.database import chats_collection, qa_collection
# Import ObjectId to convert standard string IDs to MongoDB's internal ObjectId format
from bson.objectid import ObjectId
# Import datetime to attach timestamps to our database records
from datetime import datetime

# Function to create a brand new chat session
def create_chat(title: str):
    # Define the document structure for the new chat
    chat_doc = {
        "title": title, # Set the chat title
        "created_at": datetime.utcnow(), # Set the creation time to right now
        "qa_refs": [] # Start with an empty list of Q&A references
    }
    # Insert the document into the chats collection
    result = chats_collection.insert_one(chat_doc)
    # Return the generated ID as a string so it can be used elsewhere
    return str(result.inserted_id)

# Function to save a question and answer, and link it to an existing chat
def add_qa_to_chat(chat_id: str, question: str, answer: str):
    # Define the document structure for the Q&A pair
    qa_doc = {
        "chat_id": ObjectId(chat_id), # Link it to the parent chat using ObjectId
        "question": question, # Save the user's question
        "answer": answer, # Save the AI's answer
        "timestamp": datetime.utcnow() # Save the exact time this happened
    }
    # Insert the Q&A document into the qa_pairs collection
    result = qa_collection.insert_one(qa_doc)
    # Extract the ID of the newly inserted Q&A pair
    qa_id = str(result.inserted_id)
    
    # Update the parent chat document to include this new Q&A reference
    chats_collection.update_one(
        {"_id": ObjectId(chat_id)}, # Find the chat by its ID
        {"$push": {"qa_refs": ObjectId(qa_id)}} # Push the new Q&A ID into the qa_refs array
    )
    # Return the Q&A ID
    return qa_id

# Function to fetch all chat sessions (used for the history sidebar)
def get_all_chats():
    # Fetch all documents from the chats collection and sort them newest to oldest
    chats = chats_collection.find().sort("created_at", -1)
    
    # Initialize an empty list to hold the formatted results
    result = []
    # Loop through each chat fetched from the database
    for chat in chats:
        # Append a cleanly formatted dictionary to our result list
        result.append({
            "id": str(chat["_id"]), # Convert ObjectId back to a string
            "title": chat.get("title", "Untitled Chat"), # Get the title or a default value
            "created_at": chat["created_at"], # Keep the timestamp
            # Convert all ObjectId references in the array back to strings
            "qa_refs": [str(ref) for ref in chat.get("qa_refs", [])]
        })
    # Return the list of all chats
    return result

# Function to fetch a specific chat and ALL its past messages (used when clicking a chat in history)
def get_chat_with_qa(chat_id: str):
    # Find the specific chat document using its ID
    chat = chats_collection.find_one({"_id": ObjectId(chat_id)})
    # If the chat doesn't exist, return None
    if not chat:
        return None
    
    # Fetch all Q&A pairs that belong to this chat, sorted chronologically
    qa_pairs = qa_collection.find({"chat_id": ObjectId(chat_id)}).sort("timestamp", 1)
    
    # Initialize an empty list to hold the formatted Q&A pairs
    qa_list = []
    # Loop through each Q&A pair
    for qa in qa_pairs:
        # Append the formatted Q&A data to our list
        qa_list.append({
            "id": str(qa["_id"]), # Convert ObjectId to string
            "question": qa["question"],
            "answer": qa["answer"],
            "timestamp": qa["timestamp"]
        })
        
    # Return the complete package: the chat info PLUS all the actual messages
    return {
        "id": str(chat["_id"]),
        "title": chat.get("title", "Untitled Chat"),
        "created_at": chat["created_at"],
        "qa_refs": [str(ref) for ref in chat.get("qa_refs", [])],
        "qa_pairs": qa_list # The fully loaded messages
    }

# Function to delete a chat and all its associated Q&A pairs
def delete_chat(chat_id: str):
    try:
        # 1. Delete all Q&A pairs that belong to this chat
        qa_collection.delete_many({"chat_id": ObjectId(chat_id)})
        
        # 2. Delete the parent chat document itself
        result = chats_collection.delete_one({"_id": ObjectId(chat_id)})
        
        # Return true if a chat was actually deleted
        return result.deleted_count > 0
    except Exception as e:
        # Catch invalid ObjectIds or database errors
        return False

# Function to rename a chat
def update_chat_title(chat_id: str, new_title: str):
    try:
        result = chats_collection.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"title": new_title}}
        )
        return result.modified_count > 0
    except Exception as e:
        return False

# Function to fetch the most recent N Q&A pairs for a chat (used for LLM conversation context)
def get_recent_history(chat_id: str, limit: int = 5):
    try:
        # Fetch the last `limit` Q&A pairs for this chat, sorted oldest-first so the LLM sees them in order
        qa_pairs = list(
            qa_collection.find({"chat_id": ObjectId(chat_id)})
            .sort("timestamp", -1)  # newest first
            .limit(limit)
        )
        # Reverse so the oldest message comes first (natural conversation order)
        qa_pairs.reverse()
        
        # Return a simple list of question/answer dicts for the LLM
        return [{"question": qa["question"], "answer": qa["answer"]} for qa in qa_pairs]
    except Exception as e:
        return []
