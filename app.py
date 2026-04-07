from fastapi import FastAPI, Request, HTTPException
from utils.sql_utils import *
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 6969))

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/folders", status_code=201)
async def create_folder_api(request: Request):
    body = await request.json()
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    description = body.get("description")
    create_folder(name, description)
    return {"message": "folder created"}

@app.get("/folders")
def get_folders_api():
    return get_folders()

@app.post("/notes", status_code=201)
async def create_note_api(request: Request):
    body = await request.json()
    folder_id = body.get("folder_id")
    title = body.get("title")
    content = body.get("content")
    if not folder_id:
        raise HTTPException(status_code=400, detail="folder_id is required")
    create_note(folder_id, title, content)
    return {"message": "note created"}

@app.get("/notes")
def get_notes_api():
    return get_notes()

@app.get("/notes/{folder_id}")
def get_notes_folder_api(folder_id: int):
    return get_notes_by_folder(folder_id)

@app.put("/folders/{folder_id}")
async def update_folder_api(folder_id: int, request: Request):
    body = await request.json()
    name = body.get("name")
    description = body.get("description")
    updated = update_folder(folder_id, name, description)
    if not updated:
        raise HTTPException(status_code=404, detail="Folder not found")
    return {"message": "folder updated"}

@app.delete("/folders/{folder_id}")
def delete_folder_api(folder_id: int):
    delete_folder(folder_id)
    return {"message": "folder deleted"}

@app.put("/notes/{note_id}")
async def update_note_api(note_id: int, request: Request):
    body = await request.json()
    title = body.get("title")
    content = body.get("content")
    folder_id = body.get("folder_id")
    updated = update_note(note_id, folder_id, title, content)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "note updated"}

@app.delete("/notes/{note_id}")
def delete_note_api(note_id: int):
    delete_note(note_id)
    return {"message": "note deleted"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=False
    )
