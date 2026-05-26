# 🧠 Full-Stack LLM Chatbot - Backend Guide

This is the fully functioning backend for your Chatbot. Below is an explanation of **how the code works file-by-file**, how to run it, and what you need to do next for the frontend.

---

## 🏗 Backend Code Explanation (File-by-File)

### 1. The Entry Point: `main.py`
This is where the FastAPI server is initialized. 
- It configures **CORS** (`CORSMiddleware`) so your frontend (HTML/JS) is allowed to talk to the backend without throwing security errors.
- It registers the two routers using `app.include_router(chat.router)` and `app.include_router(history.router)`.

### 2. Configuration: `config/settings.py` & `.env`
- The `.env` file holds your secrets (`GROQ_API_KEY` and `MONGO_URI`).
- `config/settings.py` uses `python-dotenv` to read those secrets into a `Settings` class, ensuring we never hardcode passwords directly into our logic.

### 3. Database Connection: `db/database.py`
- We use **PyMongo** (synchronous MongoDB client) to connect to your database using the URI from `settings.py`.
- It creates two collections:
  - `chats_collection`: Stores the overall Chat Sessions.
  - `qa_collection`: Stores every single Question/Answer pair.

### 4. Database Operations: `db/crud.py`
This file contains the queries that speak to MongoDB:
- `create_chat()`: Creates a new chat session and gives it a title based on the user's first question.
- `add_qa_to_chat()`: Inserts the new Q&A pair into `qa_collection`, and then updates the `chats_collection` by adding the new QA ID into its `qa_refs` array.
- `get_all_chats()`: Fetches all chat sessions, sorted by newest first.
- `get_chat_with_qa()`: Fetches a specific chat session AND uses the `chat_id` to query `qa_collection` for all the questions and answers that belong to it.
- `delete_chat()`: Deletes both the parent chat document and all of its associated Q&A pairs from the database to prevent orphaned records.

### 5. Data Validation: `models/schema.py`
FastAPI uses **Pydantic** to make sure incoming data is correct.
- `ChatRequest`: Ensures the frontend sends a `question` (string). It also accepts an optional `chat_id` (if the user is continuing a previous conversation).
- The other schemas (`ChatResponse`, `ChatDetailResponse`) dictate exactly what JSON shape is sent back to the frontend.

### 6. External APIs: `services/llm_service.py`
- Connects to **Groq**.
- The `get_llm_response()` function takes the user's question, sends it to the modern `llama-3.1-8b-instant` model, and returns the generated text answer.

### 7. Core Logic: `services/chat_service.py`
This is the "Brain" linking the LLM and the DB. 
- It first calls Groq (`get_llm_response()`) to get the answer.
- If the frontend didn't provide a `chat_id`, it creates a new chat in the DB.
- It then saves the Q&A pair to the database and returns everything to the route.

### 8. Endpoints: `routes/chat.py` & `routes/history.py`
These are the API endpoints exposed to the internet.
- `POST /chat`: Receives the user question, calls the `chat_service`, and returns the LLM's answer.
- `GET /history`: Returns a list of all chats.
- `GET /history/{chat_id}`: Returns a specific chat with all of its Q&A history fully loaded.
- `DELETE /history/{chat_id}`: Deletes a specific chat session and all its messages.

---

## 🚀 How to Run the Server

1. **Set your keys**: Open `backend/.env` and enter your actual `GROQ_API_KEY` and `MONGO_URI`.
2. Open your terminal in the `backend/` folder.
3. Activate your virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt` (You've already done this!)
5. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```
6. Visit the interactive API Docs at **`http://127.0.0.1:8000/docs`** to test your backend without even needing a frontend!

---

## ✅ Frontend Integration Complete

The frontend has been completely built and integrated using **Vanilla HTML/JS** and **Tailwind CSS v4**. 
You can find the entire frontend UI implementation inside the `frontend/` directory, complete with its own dedicated `README.md` detailing the architecture, state management, and sequence flows.
