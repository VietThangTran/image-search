import os
from google import genai
from google.genai import types
from .base_model import AIBaseModel
from pydantic import BaseModel
from typing import TypeVar, Type
from PIL import Image, ImageFile

DataModel = TypeVar("DataModel", bound=BaseModel)


def image_to_base64(image_path: str) -> ImageFile:
    size = (int(os.environ["IMAGE_WIDTH"]), int(os.environ["IMAGE_HEIGHT"]))
    return Image.open(image_path).resize(size)

class Gemini(AIBaseModel):
    def __init__(self):
        super().__init__()
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        self.model = os.environ.get("GEMINI_MODEL")

    def upload_image(self, image_path: str):
        return self.client.files.upload(
            file=image_path
        )

    def generate(self, prompt: str, image_path: str = None, data_model: Type[DataModel] = None):
        # image = self.upload_image(image_path)
        # print(f"Image uploaded {image_path}")
        if image_path:
            contents = [
                Image.open(image_path),
                prompt
            ]
        else:
            contents = [
                prompt
            ]

        if data_model:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=data_model
                )
            )
        else:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        return response