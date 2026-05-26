# Import APIRouter to create modular routes for FastAPI
from fastapi import APIRouter
# Import our Pydantic schema to validate incoming data
from models.schema import ChatRequest
# Import our core business logic
from services.chat_service import process_chat

# Initialize the router for chat-related endpoints
router = APIRouter()

# Define a POST endpoint at the path "/chat"
@router.post("/chat")
# The 'req' parameter expects data matching the ChatRequest schema (question and optional chat_id)
def chat_endpoint(req: ChatRequest):
    # Call our service function, passing the question and chat_id from the frontend
    result = process_chat(req.question, req.chat_id)
    # Return the dictionary (FastAPI automatically converts this to JSON for the frontend)
    return result
