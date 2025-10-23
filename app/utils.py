import datetime
from .database import summaries_collection


sessions = {}  


async def get_or_create_session(user_id: str):
    if user_id not in sessions:
        sessions[user_id] = []
    return sessions[user_id]


async def append_message(user_id: str, role: str, text: str):
    if user_id not in sessions:
        sessions[user_id] = []
    sessions[user_id].append({"role": role, "text": text})


async def finalize_session(user_id: str, summary: str, username: str):
    """
    Store or update the session summary for a given username.
    If a summary already exists for this username, update it.
    Otherwise, create a new document.
    """
    await summaries_collection.update_one(
        {"username": username}, 
        {
            "$set": {
                "user_id": user_id,
                "summary": summary,
                "updated_at": datetime.datetime.utcnow()
            },
            "$setOnInsert": {
                "created_at": datetime.datetime.utcnow()
            }
        },
        upsert=True  # create if not exists
    )
    # Clear in-memory session
    sessions.pop(user_id, None)

# utils.py (add this)
from .database import summaries_collection

async def get_user_summary(username: str):
    """
    Retrieve existing summary for the given username.
    Returns None if not found.
    """
    doc = await summaries_collection.find_one({"username": username})
    if doc:
        return doc.get("summary")
    return None
