from pydantic import BaseModel

class JobSkills(BaseModel):
    skills:list[str]