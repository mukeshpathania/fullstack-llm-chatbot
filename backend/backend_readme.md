# 📘 Backend Development Guide (Phase 2)
## LLM Integration + Database + Async Concepts

---

## 1. 🧠 What You Will Build Now

At this stage, your APIs already exist. Now you will:
- Connect database (MongoDB / SQL)
- Integrate LLM using Groq  
- Use .env for secure configs  
- Structure backend professionally  
- Understand async programming (async/await)  
- Use Pydantic for validation  

---

## 2. ⚡ Async Programming (Very Important)

### 🔹 What is Async?

Normally:
- Code runs line by line (synchronous)  
- One task blocks another  

Async allows:
- Handle multiple requests without blocking  

---

### 🔹 Why FastAPI uses async?

FastAPI is built for high performance:
- Uses async functions  
- Handles multiple users efficiently  

---

### 🔹 Basic Syntax

python async def my_function():     return "Hello" 

---

### 🔹 Using await

python async def get_data():     result = await some_async_function()     return result 

👉 await means:
- "Wait for this task, but don’t block the whole server"

---

### 🔹 Real Use Case (LLM Call)

python async def generate_response(question: str):     response = await llm_client.ask(question)     return response 

---

## 3. 🧾 Pydantic (Data Validation)

FastAPI uses Pydantic to:
- Validate request data  
- Define schemas  

---

### 🔹 Example Schema

python from pydantic import BaseModel  class ChatRequest(BaseModel):     question: str  class ChatResponse(BaseModel):     answer: str 

---

### 🔹 Use in Route

python @router.post("/chat") async def chat(req: ChatRequest):     return {"answer": "response"} 

👉 Automatically validates:
- Missing fields  
- Wrong data types  

---

## 4. 🔐 Using .env File

### 🔹 Why?

Never hardcode:
- API keys  
- DB URLs  

---

### 🔹 Example .env

GROQ_API_KEY=your_key_here MONGO_URI=your_db_url

---

### 🔹 Load in Python

Install:
pip install python-dotenv

---

### 🔹 Usage

python from dotenv import load_dotenv import os  load_dotenv()  GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

---

### 🔹 Best Practice

Create a config file:

📁 config/settings.py

python from dotenv import load_dotenv import os  load_dotenv()  class Settings:     GROQ_API_KEY = os.getenv("GROQ_API_KEY")     MONGO_URI = os.getenv("MONGO_URI")  settings = Settings() 

---

## 5. 🤖 LLM Integration (Groq)

### 🔹 Install Client

pip install groq

---

### 🔹 Basic Usage

python from groq import Groq from config.settings import settings  client = Groq(api_key=settings.GROQ_API_KEY)  async def get_llm_response(question: str):     response = client.chat.completions.create(         model="llama3-8b-8192",         messages=[             {"role": "user", "content": question}         ]     )          return response.choices[0].message.content 

---

### 🔹 Important Note
- This call is network I/O
- Can be wrapped in async or run in threadpool  

---

## 6. 🗄️ Database Integration

### Option: MongoDB (Recommended)

Install:
pip install motor

---

### 🔹 Connection File

📁 db/database.py

python from motor.motor_asyncio import AsyncIOMotorClient from config.settings import settings  client = AsyncIOMotorClient(settings.MONGO_URI) db = client.chatbot_db  chat_collection = db["chats"] 

---

### 🔹 Insert Data

python async def save_chat(question, answer):     doc = {         "question": question,         "answer": answer     }     result = await chat_collection.insert_one(doc)     return str(result.inserted_id) 

---

### 🔹 Fetch Data

python async def get_history():     chats = []     async for doc in chat_collection.find():         chats.append(doc)     return chats 

---

## 7. 🔗 Connecting Everything (Service Layer)

📁 services/chat_service.py

python from services.llm_service import get_llm_response from db.database import save_chat  async def process_chat(question: str):     answer = await get_llm_response(question)     chat_id = await save_chat(question, answer)          return {         "id": chat_id,         "answer": answer     } 

---

## 8. 🌐 Route Integration

📁 routes/chat.py

python from fastapi import APIRouter from models.schema import ChatRequest from services.chat_service import process_chat  router = APIRouter()  @router.post("/chat") async def chat(req: ChatRequest):     return await process_chat(req.question) 

---

## 9. 🧩 Connecting to main.py

📁 main.py

python from fastapi import FastAPI from routes import chat, history  app = FastAPI()  app.include_router(chat.router) app.include_router(history.router) 

---

## 10. 🏗️ Advanced Backend Folder Structure
backend/

├── main.py                 # Entry point
│
├── routes/                 # API layer
│   ├── chat.py
│   ├── history.py
│
├── services/               # Business logic
│   ├── chat_service.py
│   ├── llm_service.py
│
├── db/                     # Database layer
│   ├── database.py
│   ├── crud.py             # DB operations
│
├── models/                 # Pydantic schemas
│   ├── schema.py
│
├── config/                 # Config management
│   ├── settings.py
│
├── utils/                  # Helpers
│   ├── logger.py
│   ├── helpers.py
│
├── core/                   # Advanced (optional)
│   ├── security.py
│   ├── middleware.py
│
└── .env
---

## 11. 📦 What Each Layer Does

### 🔹 routes/
- Handles HTTP requests  
- Calls services  

---

### 🔹 services/
- Core logic  
- Combines DB + LLM  

---

### 🔹 db/
- Only database operations  
- No business logic  

---

### 🔹 models/
- Request/Response schemas  

---

### 🔹 config/
- Environment + settings  

---

### 🔹 utils/
- Reusable helper functions  

---

## 12. ⚠️ Best Practices

- Keep routes thin  
- Put logic in services  
- Use async everywhere possible  
- Never expose API keys  
- Validate all inputs with Pydantic  

---

## 13. 🚀 Final Flow

1. User sends request  
2. Route receives request  
3. Service processes it  
4. LLM generates response  
5. DB stores chat  
6. Response returned  

---

## ✅ Outcome

By completing this phase, you will:
- Build scalable backend APIs  
- Understand async systems  
- Work with real LLM APIs  
- Structure production-level backend  

---

**End of Backend Guide