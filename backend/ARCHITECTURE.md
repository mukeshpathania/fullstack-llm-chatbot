# 🏗️ Backend Architecture & Infrastructure

This document visualizes the entire infrastructure and data flow of the LLM Chatbot Backend. We use diagrams to explain how the pieces connect so anyone can understand it at a glance!

## 1. High-Level System Architecture

This diagram shows how all the major pieces of technology interact.

```mermaid
graph TD
    %% Define Node Colors
    classDef frontend fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff;
    classDef backend fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    classDef db fill:#f39c12,stroke:#d35400,stroke-width:2px,color:#fff;
    classDef llm fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff;

    UI["Frontend (HTML/JS)"]:::frontend
    
    subgraph FastAPI Backend Server
        API["main.py (FastAPI Routes)"]:::backend
        Service["services/ (Business Logic)"]:::backend
        CRUD["db/crud.py (Data Layer)"]:::backend
    end
    
    Groq["Groq API (Llama 3 LLM)"]:::llm
    Mongo["MongoDB (Database)"]:::db

    %% Connections
    UI -- "HTTP POST /chat" --> API
    API -- "Process Request" --> Service
    Service -- "Prompt (Question)" --> Groq
    Groq -- "Generated Answer" --> Service
    Service -- "Save Data" --> CRUD
    CRUD -- "Insert/Update" --> Mongo
```

---

## 2. Request Data Flow (Step-by-Step)

What exactly happens under the hood when a user types a question and clicks "Send"?

```mermaid
sequenceDiagram
    participant User as Frontend UI
    participant Route as routes/chat.py
    participant ChatService as services/chat_service.py
    participant LLM as Groq API
    participant DB as MongoDB

    User->>Route: POST /chat { "question": "What is AI?", "chat_id": null }
    Route->>ChatService: process_chat("What is AI?", null)
    
    %% Getting AI Response
    rect rgb(240, 248, 255)
        Note right of ChatService: 1. Send Prompt to AI
        ChatService->>LLM: get_llm_response("What is AI?")
        LLM-->>ChatService: "AI stands for Artificial Intelligence..."
    end
    
    %% Database Operations
    rect rgb(255, 245, 238)
        Note right of ChatService: 2. Save to Database
        ChatService->>DB: create_chat("What is AI?...")
        DB-->>ChatService: Returns new chat_id (e.g., 123)
        ChatService->>DB: add_qa_to_chat(123, "What is AI?", "AI stands for...")
        DB-->>ChatService: Returns new qa_id (e.g., 456)
    end
    
    Note right of ChatService: 3. Return to User
    ChatService-->>Route: Return {chat_id: 123, qa_id: 456, answer: "AI stands for..."}
    Route-->>User: JSON Response Displayed on Screen
```

---

## 3. Database Schema (Entity-Relationship)

We use two distinct collections in MongoDB to keep the data clean and relational, making it highly scalable.

```mermaid
erDiagram
    CHATS {
        ObjectId _id PK "Unique Chat Session ID"
        string title "Auto-generated from first question"
        datetime created_at "Timestamp of creation"
        ObjectId[] qa_refs "List of references to QA Pairs"
    }

    QA_PAIRS {
        ObjectId _id PK "Unique Message ID"
        ObjectId chat_id FK "Reference to Parent Chat"
        string question "The User's Prompt"
        string answer "The AI's Response"
        datetime timestamp "When this message occurred"
    }

    CHATS ||--o{ QA_PAIRS : "Contains (1 to Many)"
```

---

## 4. Code Layering Architecture (Onion Model)

The code is strictly separated into modular layers. We do this so that the database code never accidentally mixes with the routing code.

```mermaid
graph LR
    classDef router fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff;
    classDef service fill:#f1c40f,stroke:#f39c12,stroke-width:2px,color:#fff;
    classDef data fill:#34495e,stroke:#2c3e50,stroke-width:2px,color:#fff;

    Routes["1. Routes Layer\n(routes/chat.py)\nHandles Web Traffic"]:::router --> Services["2. Service Layer\n(services/chat_service.py)\nHandles Brain Logic"]:::service
    Services --> Database["3. Data Layer\n(db/crud.py)\nHandles Storage"]:::data
```

### Why is it built this way?
1. **Modularity**: If you ever want to change Groq to OpenAI, you *only* touch `llm_service.py`. The rest of the app doesn't care!
2. **Database Swapping**: If you ever want to switch from MongoDB to PostgreSQL, you *only* touch `db/crud.py` and `db/database.py`. The routing and services don't change.
3. **Data Validation**: The Pydantic models sit as gatekeepers between the Frontend and the Routes layer, ensuring no bad data ever reaches the database.
