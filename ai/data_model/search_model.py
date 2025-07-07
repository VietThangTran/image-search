from pydantic import BaseModel, Field, field_validator
from typing import List

class Keywords(BaseModel):
    """Represents a list of single-word keywords in base form that identify the product in the image, including its brand and core attributes."""
    keywords: List[str] = Field(
        ...,
        description="A list of 5 unique, single-word keywords (in base form) that identify the product in the image — including its brand and essential features."
    )




