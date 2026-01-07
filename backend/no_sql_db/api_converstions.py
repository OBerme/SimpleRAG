from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import uuid

app = FastAPI()

# Configuración de MongoDB
# Nota: He puesto 'mongodb' como host porque suele ser el nombre del servicio en el docker-compose
MONGO_URL = "mongodb://admin:tu_password_seguro@mongodb:27017/"
client = AsyncIOMotorClient(MONGO_URL)
db = client["chatbot_db"]
conversations_col = db["conversations"]

# --- MODELOS DE DATOS (Basados en tu esquema) ---

class Message(BaseModel):
    # Generamos un ID único para cada mensaje como pide tu esquema
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(BaseModel):
    title: str
    user_id: str  # Relación obligatoria con User según tu diagrama

# --- HELPERS ---

def conversation_helper(conv) -> dict:
    return {
        "id": str(conv["_id"]),
        "title": conv["title"],
        "user_id": conv["user_id"],
        "created_at": conv["created_at"],
        "updated_at": conv["updated_at"],
        "messages": conv.get("messages", [])
    }

# --- ENDPOINTS ---

@app.post("/conversations/create")
async def create_conversation(conversation: ConversationCreate):
    """Crea una Conversation vinculada a un User [1,N] -> [1,1]"""
    new_conv = {
        "title": conversation.title,
        "user_id": conversation.user_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "messages": []
    }
    
    result = await conversations_col.insert_one(new_conv)
    return {"conversation_id": str(result.inserted_id), "message": "Conversación creada exitosamente"}

@app.get("/conversations/list/{user_id}")
async def list_conversations(user_id: str):
    """Lista las conversaciones de un usuario específico"""
    cursor = conversations_col.find({"user_id": user_id}).sort("updated_at", -1)
    conversations = []
    async for conv in cursor:
        data = conversation_helper(conv)
        data["message_count"] = len(data["messages"])
        del data["messages"]
        conversations.append(data)
    return {"conversations": conversations}

@app.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, message_data: Message):
    """Añade un Message a una Conversation [1,N] -> [1,1]"""
    try:
        obj_id = ObjectId(conversation_id)
    except:
        raise HTTPException(status_code=400, detail="ID de conversación no válido")

    # Convertimos el modelo Pydantic a diccionario para MongoDB
    new_message = message_data.dict()

    result = await conversations_col.update_one(
        {"_id": obj_id},
        {
            "$push": {"messages": new_message},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    return {"message_id": new_message["id"], "status": "Mensaje guardado"}

@app.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    """Obtiene todos los mensajes de una conversación"""
    try:
        conv = await conversations_col.find_one({"_id": ObjectId(conversation_id)})
    except:
        raise HTTPException(status_code=400, detail="ID no válido")

    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    return {"messages": conv.get("messages", [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)