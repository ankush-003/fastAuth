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

class UserInDB(User):
    hashed_pwd: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
coauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# the password is hashed and stored in the database, later when the user tries to login the password is hashed and compared with the hashed password in the database
def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_password_hash(pwd):
    return pwd_context.hash(pwd)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        # as the model accepts only the fields in the model, we are converting the dict to a model
        return UserInDB(**user_data)

def authenticate_user(db, username: str, pwd: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(pwd, user.hashed_pwd):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

asyn def get_current_user(token: str = Depends(coauth2_scheme), db: dict = Depends(get_db)):