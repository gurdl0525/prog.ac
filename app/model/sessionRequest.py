from pydantic import BaseModel


class sessionRequest(BaseModel):
    session_key: str
