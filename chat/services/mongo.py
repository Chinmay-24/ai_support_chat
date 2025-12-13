from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
    return _client

def get_db():
    return get_client()[settings.MONGODB_DB_NAME]

# Collection: messages
def get_messages_collection():
    db = get_db()
    return db["messages"]

def save_message(role, content, conversation_id):
    col = get_messages_collection()
    doc = {
        "role": role,  # "user" or "assistant"
        "content": content,
        "conversation_id": conversation_id,
        "created_at": datetime.utcnow(),
    }
    result = col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc

def get_conversation_messages(conversation_id, limit=20):
    col = get_messages_collection()
    cursor = col.find(
        {"conversation_id": conversation_id}
    ).sort("created_at", 1).limit(limit)
    return list(cursor)

def list_conversations():
    col = get_messages_collection()
    # Get unique conversation ids
    return col.distinct("conversation_id")