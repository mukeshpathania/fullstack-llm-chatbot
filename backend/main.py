# Import the core FastAPI class
from fastapi import FastAPI
# Import CORS middleware to allow the frontend to talk to this backend safely
from fastapi.middleware.cors import CORSMiddleware
# Import our modular routers
from routes import chat, history

# Initialize the FastAPI application with a custom title
app = FastAPI(title="LLM Chatbot API")

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allow requests from any origin ("*"). In production, you would restrict this to your actual frontend URL.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach the chat router so the "/chat" endpoint becomes active
app.include_router(chat.router)
# Attach the history router so the "/history" endpoints become active
app.include_router(history.router)

# Define a simple "root" endpoint to verify the server is running
@app.get("/")
def read_root():
    # When you visit http://127.0.0.1:8000/, this JSON will appear
    return {"message": "Backend is running!"}
