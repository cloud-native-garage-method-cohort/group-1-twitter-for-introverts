from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import pendulum


from app.diags import get_example_diagram

#
# AUTHENTICATION
#

# TODO: replace this --> kubernetes secret

SECRET_KEY = "aca7fb4df53479fc80c889c4349fde5f8aca94420ff3536b2a9e0f87b6f8c57d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# TODO: use some other kind of user dir

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$nuKdWjDBptulAHYntJi90OGhb2uSSCM4SePkaZ/Bq1QkmGweqOFsa",
        "disabled": False,
    },
    "janedoe": {
        "username": "janedoe",
        "full_name": "Jane Doe",
        "email": "janedoe@example.com",
        "hashed_password": "$2b$12$nuKdWjDBptulAHYntJi90OGhb2uSSCM4SePkaZ/Bq1QkmGweqOFsa",
        "disabled": False,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


#
# Some example methods
#


@app.get(
    "/hello_diagram",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def diagram(
    current_user: User = Depends(get_current_active_user),
):
    image_bytes: bytes = get_example_diagram()

    return Response(content=image_bytes, media_type="image/png")


#
# KUBERNETES and misc
#


client = Cloudant.iam(
    "b0582852-4032-4e6a-9bad-24f684aec520-bluemix",
    "Z_noNs4OPhDGYd7ZEkudJi-qytdR_OUekHqWR-VI_mKP",
    connect=True,
)
client.connect()

mydemo = client.create_database("tweets")


@app.post("/")
def post(message: str):
    mydemo.create_document({"message": message, "date": pendulum.now().to_w3c_string()})


@app.get("/")
def get():
    return "Welcome"


@app.get("/posts")
def get_posts(message: str):
    return mydemo.all_docs()


@app.get("/post_count")
def count(posts):
    return {"Count": mydemo.all_docs().get("total_rows")}


@app.get("/healthz")
def health_check_for_kubernetes():
    return {"isHealthy": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
