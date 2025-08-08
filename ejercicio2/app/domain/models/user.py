from pydantic import BaseModel

class User(BaseModel):
    id: int
    client_id: str
