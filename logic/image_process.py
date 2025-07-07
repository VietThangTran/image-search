from search.image_search import generate_keywords
from database import database
from fastapi import UploadFile, File
from sql import (
    INSERT_IMAGE,
    SEARCH_UPLOADED_IMAGE,
    SEARCH_SEARCHED_IMAGE,
    SEARCH_KEYWORDS,
    INSERT_KEYWORDS,
    MAPPING_KEYWORDS_IMAGES,
    GET_IMAGE_ID,
    GET_KEYWORD_IDS,
    FIND_KEYWORDS_BY_IMAGE,
    SEARCH_IMAGE_BY_IMAGE,
    UPDATE_IMAGE_STATUS
)

def insert_keywords(file_path: str):
    # Generate keywords
    keywords = generate_keywords(file_path)
    keywords = [formatted_keyword for keyword in keywords for formatted_keyword in keyword.strip().lower().split(' ')]

    # Validate keywords
    existing_keywords = database.query(
        SEARCH_KEYWORDS.format(keywords=', '.join([f"'{keyword}'" for keyword in keywords])))
    existing_keywords = [keyword[0] for keyword in existing_keywords]
    new_keywords = [keyword for keyword in keywords if keyword not in existing_keywords]
    if new_keywords:
        # Insert keywords to database
        keywords_data = ', '.join([f"('{formatted_keyword}')" for keyword in new_keywords for formatted_keyword in keyword.strip().split(' ')])
        database.query(INSERT_KEYWORDS.format(keywords=keywords_data))

    # Mapping keywords to image
    image_id = database.query(GET_IMAGE_ID.format(image_path=file_path))[0][0]
    keyword_ids = database.query(GET_KEYWORD_IDS.format(keywords=', '.join([f"'{formatted_keyword}'" for keyword in keywords for formatted_keyword in keyword.strip().split(' ')])))
    image_keywords_data = ', '.join([f"({image_id}, {keyword_id[0]})" for keyword_id in keyword_ids])
    database.query(MAPPING_KEYWORDS_IMAGES.format(keywords_images=image_keywords_data))

def process_image(file_path: str, file: UploadFile = File(...)):
    # Check if file already exists
    if len(database.query(SEARCH_UPLOADED_IMAGE.format(image_path=file_path))) < 1:
        # Insert image to database
        database.query(INSERT_IMAGE.format(image_path=file_path, image_type='UPLOAD'))

        # Insert keywords to database
        insert_keywords(file_path)

        # Update image status
        database.query(UPDATE_IMAGE_STATUS.format(image_path=file_path))

        print(f"Done processing {file_path}")

def searching_image(file_path: str, file: UploadFile = File(...)):
    # Check if file already exists
    not_exist_uploaded = len(database.query(SEARCH_UPLOADED_IMAGE.format(image_path=file_path))) < 1
    not_exist_searched = len(database.query(SEARCH_SEARCHED_IMAGE.format(image_path=file_path))) < 1
    if not_exist_uploaded and not_exist_searched:

        # Insert image to database
        database.query(INSERT_IMAGE.format(image_path=file_path, image_type='SEARCH'))

        # Insert keywords to database
        insert_keywords(file_path)

        # Update image status
        database.query(UPDATE_IMAGE_STATUS.format(image_path=file_path))

        print(f"Done processing {file_path}")

    # Get image keywords
    keywords = database.query(FIND_KEYWORDS_BY_IMAGE.format(image_path=file_path))
    keywords = [keyword[0] for keyword in keywords]

    # Search image by keywords
    images = database.query(SEARCH_IMAGE_BY_IMAGE.format(keywords=', '.join([f"'{keyword}'" for keyword in keywords])))
    images = [image[0] for image in images]

    return images
