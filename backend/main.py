import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Url
from base62 import encode_base62

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten")
def shorten_url(long_url: str, db: Session = Depends(get_db)):
    existing = db.query(Url).filter(Url.longURL==long_url).first()
    if existing:
        return {"short_url": existing.shortURL}
    
    db_url = Url(longURL=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    db_url.shortURL = encode_base62(db_url.id)
    db.commit()

    return {"short_url": db_url.shortURL}
    
    

@app.get("/{short_url}")
def redirect_by_shorten_url(short_url: str, db: Session = Depends(get_db)):
    url_entry = db.query(Url).filter(Url.shortURL==short_url).first()
    if not url_entry:
        return {"error": "URL not found"}
    return RedirectResponse(url=url_entry.longURL, status_code=302)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
