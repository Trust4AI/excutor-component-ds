from typing import List

from pydantic import BaseModel


class Placeholder(BaseModel):
    name: str
    description: str
    values: List[str]

    class Config:
        from_attributes = True

    def __repr__(self):
        return f"Placeholder(name={self.name}, description={self.description}, values={self.values}"


class Template(BaseModel):
    id: int
    base: str
    description: str
    expected_result: str
    placeholders: list['Placeholder']

    def __repr__(self):
        return f"Template(base={self.base}, description={self.description}, placeholders={self.placeholders})"


class Output(BaseModel):
    expected_result: str
    generated_result: str
    prompt: str = None

    class Config:
        from_attributes = True
