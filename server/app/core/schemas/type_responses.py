from pydantic import BaseModel


class TypeWithImageResponse(BaseModel):
    type: str
    name: str
    desc: str
    icons: dict[str, str]
