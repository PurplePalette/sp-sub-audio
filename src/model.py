from typing import Literal, Optional

from pydantic import BaseModel


class GetRootResponse(BaseModel):
    status: Literal["ok"] = "ok"


class PostConvertParams(BaseModel):
    hash: str
    start: Optional[int] = 0
    end: Optional[int] = None


class PostConvertResponse(BaseModel):
    hash: str
