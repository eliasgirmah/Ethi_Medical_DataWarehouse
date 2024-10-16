from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, schemas
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.post("/retrieve_data/", response_class=HTMLResponse)
async def retrieve_data(request: Request, start_date: str = Form(...), end_date: str = Form(...), db: Session = Depends(get_db)):
    # Convert string dates to datetime objects
    start_date_dt = datetime.fromisoformat(start_date)
    end_date_dt = datetime.fromisoformat(end_date)

    # Retrieve data from the database based on the criteria
    messages = crud.get_messages_by_date(db, start_date=start_date_dt, end_date=end_date_dt)
    
    return templates.TemplateResponse("results.html", {"request": request, "messages": messages})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
