from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .schemas import LoginRequest, TodoUpdate

app = FastAPI()

@app.get("/")
def hello():
	return {"message": "Hello World"}
	
@app.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == body.email).first()
	if user == None:
		new_user = User(email=body.email, password=body.password)
		db.add(new_user)
		db.commit()
		return db.query(User).all()