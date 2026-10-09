from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

    @field_validator("conversation_id")
    @classmethod
    def conversation_id_must_be_alphanumeric(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("conversation_id must not be blank")
        if not value.isalnum():
            raise ValueError("conversation_id must be alphanumeric")
        return value

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("message must not be blank")
        return value


@app.post("/users/{user_id}/chat")
def chat(
    user_id: Annotated[str, Path(min_length=1, description="Unique identifier of the user")],
    request: ChatRequest,
) -> dict[str, str]:
    if user_id.strip() == "":
        raise HTTPException(status_code=422, detail="user_id must not be blank")

    return {
        "user_id": user_id,
        "conversation_id": request.conversation_id,
        "message": request.message,
    }
