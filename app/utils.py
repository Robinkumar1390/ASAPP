import datetime
from .database import summaries_collection

# In-memory sessions
sessions = {}  # key: user_id, value: list of messages

# Get active session or create
async def get_or_create_session(user_id: str):
    if user_id not in sessions:
        sessions[user_id] = []
    return sessions[user_id]

# Append message to session (in-memory)
async def append_message(user_id: str, role: str, text: str):
    if user_id not in sessions:
        sessions[user_id] = []
    sessions[user_id].append({"role": role, "text": text})

# Finalize session: store summary and clear in-memory chat
async def finalize_session(user_id: str, summary: str):
    await summaries_collection.insert_one({
        "user_id": user_id,
        "summary": summary,
        "created_at": datetime.datetime.utcnow()
    })
    sessions.pop(user_id, None)  # Clear in-memory session
