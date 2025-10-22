# 🛫 ASAPP – Airline Customer Support Chatbot

## About
AI-powered chatbot that helps airline customers get **quick, natural, and human-like responses**.  
It can handle **open-ended queries**, maintain **multi-turn conversations**, and always follow **airline policies**.

---

## Tech Stack

**Backend:** Python, FastAPI, uvicorn, Gemini AI, JWT, bcrypt  
**Database:** MongoDB, Motor, Compass  
**Frontend:** HTML, JavaScript, Tailwind, Fetch API, JWT in browser  
**Dev Tools & Security:** Python env, IDE, Postman, Git, .env, CORS  

---

## Modules

### 1️⃣ Authentication
- Secure login and registration  
- JWT-based session management  
- Stores user credentials in MongoDB  

### 2️⃣ Chat Processing
- Receives messages via FastAPI  
- Preprocesses input and sends queries to Gemini AI  
- Logs chats in MongoDB  

### 3️⃣ Session Management
- Tracks conversation history for each user  
- Maintains context across multiple messages  
- Supports multiple users and sessions  

### 4️⃣ Integration
- Connects all modules seamlessly  
- Manages data flow between frontend, backend, and Gemini AI  
- Provides RESTful endpoints  

## How It Works

1. **User logs in** via the Authentication Module  
   - JWT verifies session and access  

2. **FastAPI backend** receives the message  

3. **Chat Processing Module**  
   - Cleans and preprocesses user input  
   - Sends query to Gemini AI  

4. **Gemini AI** generates a natural, policy-compliant response  

5. **Session Management Module**  
   - Updates conversation history  
   - Maintains context for multi-turn dialogue  

6. **Integration Module** formats the response and sends it back to the user  

7. **User receives** the chatbot’s reply




