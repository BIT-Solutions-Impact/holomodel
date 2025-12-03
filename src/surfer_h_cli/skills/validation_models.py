from pydantic import BaseModel


class WebRetrievalEvaluation(BaseModel):
    task: str
    screenshots: list[str] = []
    answer: str | None = ""
    success: bool = False
    why: str = ""
    url: str = ""
