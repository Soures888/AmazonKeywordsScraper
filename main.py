from src.amazon_parser.parse_client import ParseClient
from src.utils import load_keywords
from src.models.product import ProductORM
from src.crud import product_crud
from config import Config
from db import db


if __name__ == '__main__':
    keyword_list = load_keywords('res/keywords.txt')
    db.create_tables([ProductORM])

    client = ParseClient()

    try:
        client.set_location(zip_code=Config.PARSING_ZIP_CODE)

        for keyword in keyword_list:
            keyword_data = client.parse_keyword(keyword, page_per_keyword=Config.PAGE_PER_KEYWORD)
            product_crud.create_many(obj_in_list=keyword_data)
    finally:
        db.close()