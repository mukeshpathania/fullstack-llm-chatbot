# Import BaseModel from Pydantic to create data schemas
from pydantic import BaseModel
# Import List and Optional for type hinting (specifying what type of data to expect)
from typing import List, Optional
# Import datetime to work with timestamps
from datetime import datetime

# Schema for the incoming request from the frontend when a user asks a question
class ChatRequest(BaseModel):
    # Optional chat_id. If the frontend sends null, it means start a new chat.
    chat_id: Optional[str] = None  
    # The actual question text typed by the user
    question: str

# Schema for renaming a chat
class ChatUpdateRequest(BaseModel):
    title: str

# Schema representing a single Question and Answer pair
class QAPairResponse(BaseModel):
    # Unique ID of the Q&A pair in the database
    id: str
    # The user's question
    question: str
    # The LLM's answer
    answer: str
    # The exact time this conversation turn happened
    timestamp: datetime

# Schema representing a high-level Chat session (used for listing history)
class ChatResponse(BaseModel):
    # Unique ID of the chat session
    id: str
    # The auto-generated title for the chat
    title: str
    # When the chat was created
    created_at: datetime
    # A list of IDs linking to the Q&A pairs that belong to this chat
    qa_refs: List[str]  

# Schema for full Chat Details (used when the user clicks on a chat from the history sidebar)
# It inherits from ChatResponse and adds the fully loaded Q&A pairs
class ChatDetailResponse(ChatResponse):
    # A list containing the actual Q&A data, not just their IDs
    qa_pairs: List[QAPairResponse]
