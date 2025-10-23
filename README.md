# 🛫 ASAPP – Airline Customer Support Chatbot

## About
AI-powered chatbot that helps airline customers get **quick, natural, and human-like responses**.  
It can handle **open-ended queries**, maintain **multi-turn conversations**, and always follow **airline policies**.

---

## Tech Stack

**Backend:** Python, FastAPI, uvicorn, Gemini AI, JWT, bcrypt  
**Database:** MongoDB, Motor, Compass  
**Frontend:** HTML, JavaScript, Tailwind, Fetch API, JWT in browser  
**Dev Tools & Security:** Postman, Git, .env 

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

### 1. User Authentication and Login
Users log into the system via the **Authentication Module**, which ensures secure access.  
- Upon successful login, a **JWT (JSON Web Token)** is issued to verify the user session.  
- Only authenticated users can interact with the chatbot.

### 2. Message Reception
The user's message is received by the **FastAPI backend**, which acts as the central server:  
- Handles incoming requests  
- Routes queries to the appropriate processing modules  

### 3. Chat Processing Module
Before sending the message to the AI:  
- User input is **cleaned and preprocessed** (e.g., removing unwanted characters, handling typos, emojis)  
- The prepared input is forwarded to **Gemini AI** for response generation  

### 4. Gemini AI – Response Generation
**Gemini AI** generates:  
- Natural, human-like responses  
- Policy-compliant and relevant answers  
- Context-aware replies for a smooth conversational experience  

### 5. Session Management
The **Session Management Module** keeps track of the conversation:  
- Updates conversation history  
- Maintains context for multi-turn dialogues  

### 6. Integration and Response Delivery
The **Integration Module**:  
- Formats the AI-generated response for display  
- Sends the response back to the user interface  

### 7. User Receives Response
Finally, the user receives the chatbot’s reply in real time, ensuring:  
- Context-aware answers  
- Accurate, human-like conversation  
- Seamless interaction experience  





