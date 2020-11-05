from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', default=1))
    PAGE_PER_KEYWORD = int(os.environ.get('PAGE_PER_KEYWORD', default=10))
    PARSING_ZIP_CODE  = str(os.environ.get('PARSING_ZIP_CODE', default=10001))
