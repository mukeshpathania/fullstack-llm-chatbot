# Import APIRouter and HTTPException for error handling
from fastapi import APIRouter, HTTPException
# Import our database query functions
from db.crud import get_all_chats, get_chat_with_qa, delete_chat, update_chat_title
from models.schema import ChatUpdateRequest

# Initialize the router for history-related endpoints
router = APIRouter()

# Define a GET endpoint at "/history" to fetch the list of all chats
@router.get("/history")
def get_history_list():
    # Call the database function to get all chats
    chats = get_all_chats()
    # Return the list of chats to the frontend
    return chats

# Define a GET endpoint with a dynamic path parameter "{chat_id}"
@router.get("/history/{chat_id}")
# The chat_id variable is automatically extracted from the URL
def get_chat_detail(chat_id: str):
    # Call the database function to get the specific chat and all its messages
    chat = get_chat_with_qa(chat_id)
    
    # If the database returns None (meaning the chat wasn't found), throw a 404 Error
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    # Otherwise, return the chat details to the frontend
    return chat

# Define a DELETE endpoint to remove a specific chat
@router.delete("/history/{chat_id}")
def delete_chat_endpoint(chat_id: str):
    # Call the database function to delete the chat and its Q&A pairs
    success = delete_chat(chat_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found or already deleted")
        
    return {"message": "Chat deleted successfully"}

# Define a PATCH endpoint to rename a chat
@router.patch("/history/{chat_id}")
def rename_chat(chat_id: str, req: ChatUpdateRequest):
    success = update_chat_title(chat_id, req.title)
    
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found or title unchanged")
        
    return {"message": "Chat renamed successfully"}

