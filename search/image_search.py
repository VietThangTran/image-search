from ai import AIModel
from ai.data_model.search_model import Keywords

ai_model = AIModel()

def generate_keywords(image_path):
    response = ai_model.generate(
        "Extract the keywords from this image",
        image_path=image_path,
        data_model=Keywords
    )
    return response.parsed.keywords
