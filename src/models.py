from pydantic import BaseModel


class AutoPublishConfig(BaseModel):
    channels: list[str]
