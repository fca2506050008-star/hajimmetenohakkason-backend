from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .schemas import LoginRequest, TodoUpdate
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']


app = FastAPI()

@app.get("/")
def hello():
	return {"message": "Hello World"}
	
@app.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):

	# ユーザーがDBにいるかを調査
	user = db.query(User).filter(User.email == body.email).first()

	# ユーザーがいなかった場合新規作成
	if user == None:
		new_user = User(email=body.email, password=body.password)
		db.add(new_user)
		db.commit()	

	access_token = create_access_token(
        data={"sub": str(user.id)}
	)

	return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

	