let token = null;
let usernameGlobal = null; // Store username globally

const authSection = document.getElementById("auth-section");
const chatSection = document.getElementById("chat-section");
const chatContainer = document.getElementById("chat-container");
const chatInput = document.getElementById("chat-input");
const authMessage = document.getElementById("auth-message");

const API_BASE = "http://127.0.0.1:8000"; // FastAPI server

// Append message to chat
function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" 
        ? "text-right text-blue-600 mb-2" 
        : "text-left text-green-700 mb-2";
    msg.textContent = text;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Reset auth message style
function resetAuthMessage() {
    authMessage.style.color = "red";
    authMessage.textContent = "";
}

// LOGIN
document.getElementById("login-btn").addEventListener("click", async () => {
    resetAuthMessage();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    
    if (!username || !password) {
        authMessage.textContent = "Fill both fields";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            token = data.token;
            usernameGlobal = username; // store username
            authSection.classList.add("hidden");
            chatSection.classList.remove("hidden");
        } else {
            authMessage.textContent = data.detail || "Login failed";
        }
    } catch (e) {
        authMessage.textContent = "Server error";
    }
});

// SIGNUP
document.getElementById("signup-btn").addEventListener("click", async () => {
    resetAuthMessage();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        authMessage.textContent = "Fill both fields";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            authMessage.style.color = "green";
            authMessage.textContent = "Registered successfully! Login now.";
        } else {
            authMessage.textContent = data.detail || "Signup failed";
        }
    } catch (e) {
        authMessage.textContent = "Server error";
    }
});

// SEND MESSAGE
document.getElementById("send-btn").addEventListener("click", async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    chatInput.value = "";

    if (!usernameGlobal) {
        appendMessage("No user logged in", "ai");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/chat/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ 
                message, 
                username: usernameGlobal // send username for summary retrieval
            })
        });
        const data = await res.json();
        appendMessage(data.answer || "No response from server", "ai");
    } catch (e) {
        appendMessage("Error contacting server", "ai");
    }
});

// END SESSION
document.getElementById("end-btn").addEventListener("click", async () => {
    if (!usernameGlobal) {
        appendMessage("No user logged in", "ai");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/chat/end_session`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ username: usernameGlobal }) // send username
        });
        const data = await res.json();
        appendMessage("Session Ended. Summary: " + (data.summary || "N/A"), "ai");

        // Reset to login
        chatSection.classList.add("hidden");
        authSection.classList.remove("hidden");
        chatContainer.innerHTML = "";
        token = null;
        usernameGlobal = null;
    } catch (e) {
        appendMessage("Error ending session", "ai");
    }
});

// Allow Enter key to send
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") document.getElementById("send-btn").click();
});
