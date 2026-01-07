from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Configuración de MongoDB (Usa las credenciales de tu docker-compose)
MONGO_URL = "mongodb://admin:tu_password_seguro@mongodb:27017/"
client = AsyncIOMotorClient(MONGO_URL)
db = client["chatbot_db"]  # Nombre de la base de datos
conversations_col = db["conversations"] # Colección de conversaciones

# Helpers para manejar los IDs de MongoDB (ObjectIDs)
def conversation_helper(conv) -> dict:
    return {
        "id": str(conv["_id"]),
        "title": conv["title"],
        "user_id": conv["user_id"],
        "created_at": conv["created_at"],
        "updated_at": conv["updated_at"],
        "messages": conv.get("messages", [])
    }

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    title: str
    user_id: Optional[str] = "default_user"

@app.post("/conversations/create")
async def create_conversation(conversation: Conversation):
    """Crear una nueva conversación (en Mongo es un documento con lista de mensajes)"""
    new_conv = {
        "title": conversation.title,
        "user_id": conversation.user_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "messages": [] # Inicializamos la lista de mensajes vacía
    }
    
    result = await conversations_col.insert_one(new_conv)
    return {"conversation_id": str(result.inserted_id), "message": "Conversación creada"}

@app.get("/conversations/list")
async def list_conversations(user_id: str = "default_user"):
    """Listar conversaciones usando filtros de MongoDB"""
    cursor = conversations_col.find({"user_id": user_id}).sort("updated_at", -1)
    conversations = []
    async for conv in cursor:
        conv_data = conversation_helper(conv)
        conv_data["message_count"] = len(conv_data["messages"])
        del conv_data["messages"] # No enviamos los mensajes en el listado
        conversations.append(conv_data)
        
    return {"conversations": conversations}

@app.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, message: Message):
    """Añadir un mensaje usando el operador $push de MongoDB"""
    try:
        obj_id = ObjectId(conversation_id)
    except:
        raise HTTPException(status_code=400, detail="ID no válido")

    new_message = {
        "role": message.role,
        "content": message.content,
        "timestamp": datetime.utcnow()
    }

    # $push añade el mensaje al array y $set actualiza la fecha de modificación
    result = await conversations_col.update_one(
        {"_id": obj_id},
        {
            "$push": {"messages": new_message},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    return {"message": "Mensaje guardado exitosamente"}

@app.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    """Obtener los mensajes de una conversación específica"""
    try:
        conv = await conversations_col.find_one({"_id": ObjectId(conversation_id)})
    except:
        raise HTTPException(status_code=400, detail="ID no válido")

    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    # En MongoDB los mensajes ya vienen dentro del objeto conversación
    return {"messages": conv.get("messages", [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)