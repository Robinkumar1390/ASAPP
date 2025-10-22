import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.chatdb

users_collection = db.users
summaries_collection = db.summaries  
