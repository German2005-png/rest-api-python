from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

personadb = []

class Persona(BaseModel):
    id: Optional[int] = None
    user: str
    mensaje: str

class Mensaje(BaseModel):
    mensaje: str

@app.post("/persona/", response_model=Persona)
def crear_persona(persona: Persona):
    persona.id = len(personadb) + 1
    personadb.append(persona)
    return persona

@app.get("/mensaje/{persona_id}", response_model=Persona)
def obtener_mensaje(persona_id: int):
    for persona in personadb:
        if persona.id == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.get("/mensajes/", response_model=list[Persona])
def listar_personas():
    return personadb

@app.put("/mensaje/{persona_id}", response_model=Persona)
def actualizar_mensaje(persona_id: int, mensaje_actualizado: Mensaje):
    for index, persona in enumerate(personadb):
        if persona.id == persona_id:
            persona.mensaje = mensaje_actualizado.mensaje
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.delete("/mensaje/{persona_id}", response_model=Persona)
def eliminar_mensaje(persona_id: int):
    for index, persona in enumerate(personadb):
        if persona.id == persona_id:
            del personadb[index]
            return {"detail": "Persona eliminada"}
    raise HTTPException(status_code=404, detail="Persona no encontrada")