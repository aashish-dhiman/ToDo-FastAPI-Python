from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.note import Note
from config.db import client
from schemas.note import notes, noteEntity

templates = Jinja2Templates(directory="templates")

note = APIRouter()

db = client.notes


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    newDocs = []
    docs = db.notes.find({})
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "description": doc["description"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


@note.post("/")
async def add_note(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict["important"] == 'on' else False
    print(formDict)
    inserted_note = db.notes.insert_one(formDict)
    return {"Success": True}
