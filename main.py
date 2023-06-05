from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# command: openssl rand -hex 32
SECRET_KEY = "4093fa6550e83e141f53ea3c833a68c377dd59e405ee900c281af8eb7ee25d5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# data validation using pydantic
# class Data(BaseModel):
#     name: str
#
# @app.get("/test/{item_id}/")
# async def test(item_id: str, query: int | None = None):
#     return {"item_id":item_id}
#
# # since we are using pydantic it is expecting json data
# @app.post("/create/")
# def create(data: Data):
#     return {"data": data}

fake_db = {
    "ankush": {
        "username":"ankush-003",
        "full_name": "Ankush H V",
        "email": "anshhv2003@gmail.com",
        "hashed_pwd": "",
        "disabled": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None
