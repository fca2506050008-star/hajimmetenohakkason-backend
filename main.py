from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .schemas import LoginRequest, choice
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
import random


load_dotenv()
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
	else:
		if user.password != body.password:
			raise HTTPException(status_code=400, detail="パスワードが違います")


	# JWT 作成
	access_token = create_access_token(data={"sub": str(user.id)})


	# Cookie に JWT をセット
	response = Response(content = '{"message": "login successful"}')
	response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    secure=True,
    samesite="None",
    path="/api"     
	)

	return response 

	# return {"access_token": access_token, "token_type": "bearer"}




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/api/calc")
def get_random_int():
    return {"value": random.randint(4000, 30000)}


@app.post("/some-action")
def some_action(body: choice):
    if body.choice == "treat":
        return {"result": True}

    elif body.choice == "split":
        return {"result": False}

    else:
        # それ以外が来たらエラー
        raise HTTPException(status_code=400, detail="Invalid choice")
