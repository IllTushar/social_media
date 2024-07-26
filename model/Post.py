from pydantic import BaseModel
from typing import List


class ResponseClass(BaseModel):
    id: str
    captions: str
    images: str  # Assuming 'images' is a list of file paths or URLs
