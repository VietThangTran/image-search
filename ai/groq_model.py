# from base_model import AIBaseModel
# from pydantic import BaseModel
# from typing import TypeVar, Type
# from groq import Groq
# import base64
# import os
# import instructor
#
# from dotenv import load_dotenv
# from data_model.search_model import Keywords
# load_dotenv('../.env')
#
# DataModel = TypeVar("DataModel", bound=BaseModel)
#
#
# # Function to encode the image
# def encode_image(image_path: str):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')
#
# class GroqModel(AIBaseModel):
#     def __init__(self):
#         super().__init__()
#         self.client = Groq(
#             api_key=
#             os.environ.get("GROQ_API_KEY")
#         )
#         self.instructor_client = instructor.patch(self.client)
#         self.model = os.environ.get("GROQ_MODEL")
#
#     def generate(self, prompt: str, image_path: str = None, data_model: Type[DataModel] = None):
#
#         if image_path:
#             # Getting the base64 string
#             base64_image = encode_image(image_path)
#             messages = [
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64_image}",
#                             },
#                         },
#                     ],
#                 }
#             ],
#         else:
#             messages = [
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                     ],
#                 }
#             ],
#
#         if data_model:
#             response = self.instructor_client.chat.completions.create(
#                 messages=messages,
#                 model=self.model,
#                 response_model=data_model
#             )
#         else:
#             response = self.client.chat.completions.create(
#                 messages=messages,
#                 model=self.model,
#             )
#         return response
#
# groq_model = GroqModel()
# chat_completion = groq_model.generate(
#     "Extract the keywords from this image",
#     image_path="../uploads/omo-box.png",
#     data_model=Keywords
# )
# print(chat_completion.choices[0].message.content)