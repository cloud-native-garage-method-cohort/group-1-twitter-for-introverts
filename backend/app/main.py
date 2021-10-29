from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import pendulum

# TODO: replace this --> kubernetes secret

SECRET_KEY = "aca7fb4df53479fc80c889c4349fde5f8aca94420ff3536b2a9e0f87b6f8c57d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


#
# KUBERNETES and misc
#

client = Cloudant.iam(
    "b0582852-4032-4e6a-9bad-24f684aec520-bluemix",
    "Z_noNs4OPhDGYd7ZEkudJi-qytdR_OUekHqWR-VI_mKP",
    connect=True,
)
client.connect()

tweets_db = client.create_database("tweets")


# GET / -- Get all posts in DB sorted by newest first
@app.get("/")
def get_posts():
    messages_query = tweets_db.all_docs(descending=True, include_docs=True)

    def dk(elem):
        return pendulum.parse(elem["doc"]["date"])

    total_messages = messages_query["total_rows"]
    messages = messages_query["rows"]
    messages_formatted = []

    for message in sorted(messages, key=dk):
        messages_formatted.append(
            {
                "id": message["id"],
                "message": message["doc"]["message"],
                "date": message["doc"]["date"],
            }
        )

    return {"total_messages": total_messages, "messages": messages_formatted}


# POST / -- Add new post to the DB
class NewMessagePostData(BaseModel):
    message: str


@app.post("/")
def post(data: NewMessagePostData):
    if len(data.message) > 10:
        raise HTTPException(
            status_code=400,
            detail=f"You sent {len(data.message)} characters. Max 10 characters allowed!",
        )
    result = tweets_db.create_document(
        {"message": data.message, "date": pendulum.now().to_w3c_string()}
    )
    return {"success": True, "new_message": result}


# GET /readyz -- Heath check
@app.get("/readyz")
def health_check_for_kubernetes():
    return {"isHealthy": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
