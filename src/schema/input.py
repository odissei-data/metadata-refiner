from typing import Any

from pydantic import BaseModel


class RefinerInput(BaseModel):
    metadata: list | dict | Any
