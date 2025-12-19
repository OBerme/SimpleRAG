from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import json
import os

app = FastAPI()

DB_FILE = "chatbot.db"

def init_db():
    """Inicializar la base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabla de conversaciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        user_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de mensajes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    title: str
    user_id: Optional[str] = "default_user"

@app.post("/conversations/create")
async def create_conversation(conversation: Conversation):
    """Crear una nueva conversación"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    
    cursor.execute(
        "INSERT INTO conversations (title, user_id, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (conversation.title, conversation.user_id, now, now)
    )
    
    conversation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"conversation_id": str(conversation_id), "message": "Conversación creada exitosamente"}

@app.get("/conversations/list")
async def list_conversations(user_id: str = "default_user"):
    """Listar todas las conversaciones de un usuario"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        # Contar mensajes
        cursor.execute("SELECT COUNT(*) FROM messages WHERE conversation_id = ?", (row['id'],))
        count = cursor.fetchone()[0]
        
        result.append({
            "id": str(row['id']),
            "title": row['title'],
            "user_id": row['user_id'],
            "created_at": row['created_at'],
            "updated_at": row['updated_at'],
            "message_count": count
        })
    
    conn.close()
    return {"conversations": result}

@app.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, message: Message):
    """Añadir un mensaje a una conversación"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Verificar existencia
    cursor.execute("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    now = datetime.utcnow().isoformat()
    
    # Insertar mensaje
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, message.role, message.content, now)
    )
    
    # Actualizar timestamp de conversación
    cursor.execute(
        "UPDATE conversations SET updated_at = ? WHERE id = ?",
        (now, conversation_id)
    )
    
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"message_id": str(msg_id), "message": "Mensaje guardado exitosamente"}

@app.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    """Obtener todos los mensajes de una conversación"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
        (conversation_id,)
    )
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        result.append({
            "id": str(row['id']),
            "role": row['role'],
            "content": row['content'],
            "timestamp": row['timestamp']
        })
    
    conn.close()
    return {"messages": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
