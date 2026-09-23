from fastapi import FastAPI, HTTPException
from fastapi.datastructures import URL
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
app= FastAPI()
#db configuration
url= "mongodb://127.0.0.1:27017"
client = MongoClient(URL) 
db = client["service_ticket_db"]
ticket_collection = db["tickets"]

#schema pydantic
class TicketCreate(BaseModel):
    tittle :str
    description :str
    category:str
    status:str
    
class TicketResponse(TicketCreate):
    id:str
    
#helper
def ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "tittle": ticket_doc["tittle"],
        "description": ticket_doc["description"],
        "category": ticket_doc["category"],
        "status": ticket_doc["status"] 
    }

#apis - crud - create, read, update, delete
@app.get("/tickets",response_model=TicketResponse,status_code=201)
def ticket_create(payload:TicketCreate):
    ticket_dict = payload.model_dump()
    result = ticket_collection.insert_one(ticket_dict)
    new_ticket = ticket_collection.find_one({"_id": result.inserted_id})
    return ticket_helper(new_ticket)

@app.get("/tickets",response_model=list[TicketResponse])
def get_ticket_read_all():
    docs = ticket_collection.find()
    tickets = [ticket_helper(doc) for doc in docs]
    return tickets