from pydantic import BaseModel


class BrainDumpRequest(BaseModel):
    """Raw brain dump from user"""

    text: str
    user_id: int
