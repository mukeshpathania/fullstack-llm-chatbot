# 🚀 Full-Stack AI Chatbot Project

Welcome! Instead of downloading a ZIP file (which makes it hard to save your updates), please follow these simple steps to get the code using **Git**. 

This guide will show you how to download the code, run it, and push your changes to your own personal branch.

---

## 1️⃣ Get the Code (Clone)
First, open your terminal (or Command Prompt / Git Bash) and run this command to download the project directly from GitHub:
```bash
git clone <INSERT_GITHUB_REPO_URL_HERE>
cd "LLM Integration(Python)"
```
*(This pulls the exact code from GitHub onto your machine and moves you into the project folder.)*

---

## 2️⃣ Create Your Own Workspace (Branch)
We don't want everyone editing the `main` code at the same time. Create your own personal "workspace" (called a branch) using your name:
```bash
git checkout -b your-name-here
```
*(Example: `git checkout -b john-doe`. Now you are safely working in your own isolated copy of the code!)*

---

## 3️⃣ Start the Backend (Python)
You need to start the Python server so the AI can think. Open a terminal inside the `backend` folder and run:
```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # NOTE: On Windows, use `venv\Scripts\activate`

# Install required Python packages
pip install -r requirements.txt
```

**⚠️ Important:** Before starting the server, create a file named `.env` inside the `backend/` folder and paste your keys:
```env
GROQ_API_KEY=your_groq_key_here
MONGO_URI=your_mongodb_uri_here
```

Now, start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*(Leave this terminal window running! Your backend is now alive.)*

---

## 4️⃣ Start the Frontend (HTML/JS)
Open a **new** terminal window and go to the `frontend` folder:
```bash
cd frontend

# Install Tailwind CSS dependencies
npm install

# Start the Tailwind compiler so your CSS updates automatically
npm run dev
```
*(Leave this terminal window running too!)*

**To see the app:** Simply double-click the `frontend/index.html` file to open it in your Google Chrome or Safari browser!

---

## 5️⃣ Save & Push Your Work to GitHub
When you have made changes to the code (like changing the CSS colors or adding a new feature), you need to save them back to GitHub **on your specific branch**.

Run these three commands in your terminal:
```bash
# 1. Stage all your changed files
git add .

# 2. Save them locally with a brief message explaining what you did
git commit -m "Added my new UI changes"

# 3. Push YOUR branch up to GitHub (Replace 'your-name-here' with your actual branch name!)
git push origin your-name-here
```
*(Success! Your code is now safely backed up on GitHub under your name, and you didn't overwrite the main project!)*
