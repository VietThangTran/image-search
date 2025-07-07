INSERT_IMAGE = """
INSERT INTO images (image_path, image_type, status) VALUES ('{image_path}', '{image_type}', 'INDEXING');
"""

UPDATE_IMAGE_STATUS = """
UPDATE images SET status = 'DONE' WHERE image_path = '{image_path}';
"""

GET_ALL_IMAGES = """
SELECT image_path, status FROM images WHERE image_type = 'UPLOAD';
"""

SEARCH_UPLOADED_IMAGE = """
SELECT image_path FROM images WHERE image_path = '{image_path}' AND image_type = 'UPLOAD';
"""

SEARCH_SEARCHED_IMAGE = """
SELECT image_path FROM images WHERE image_path = '{image_path}' AND image_type = 'SEARCH';
"""

GET_IMAGE_ID = """
SELECT image_id FROM images WHERE image_path = '{image_path}';
"""

SEARCH_KEYWORDS = """
SELECT keyword FROM keywords WHERE keyword IN ({keywords});
"""

INSERT_KEYWORDS = """
INSERT INTO keywords (keyword) VALUES {keywords};
"""

MAPPING_KEYWORDS_IMAGES = """
INSERT INTO keywords_of_images (image_id, keyword_id) VALUES {keywords_images};
"""

GET_KEYWORD_IDS = """
SELECT keyword_id FROM keywords WHERE keyword IN ({keywords});
"""

FIND_KEYWORDS_BY_IMAGE = """
SELECT k.keyword
FROM images i
JOIN public.keywords_of_images koi on i.image_id = koi.image_id
JOIN public.keywords k on k.keyword_id = koi.keyword_id
WHERE i.image_path = '{image_path}';
"""

SEARCH_IMAGE_BY_IMAGE = """
SELECT DISTINCT i.image_path
FROM images i
JOIN public.keywords_of_images koi on i.image_id = koi.image_id
JOIN public.keywords k on k.keyword_id = koi.keyword_id
WHERE LOWER(k.keyword) IN ({keywords}) AND i.image_type = 'UPLOAD';
"""