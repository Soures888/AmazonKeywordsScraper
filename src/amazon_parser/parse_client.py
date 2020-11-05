import json
import itertools
import collections

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from typing import List, Optional
from loguru import logger

from datetime import datetime


from config import Config
from src.amazon_parser.request_executor import RequestExecutor
from src.models.product import ProductData



# Selectors data
CSS_SELECTORS = {
    'product': 'div.s-result-list.sg-row > div.s-result-item.s-asin',
    'url': 'div div a.a-link-normal',
    'badge': 'span[data-component-type="s-status-badge-component"]'
}


class ParseClient:
    def __init__(self):
        """Init a parse client with request executor"""
        self._request_executor = RequestExecutor(request_timeout=Config.REQUEST_TIMEOUT)

    def _extract_page(self, page_html: str, keyword: str, page_number: int) -> List[ProductData]:
        """Extract page to dict format with data"""

        product_data_list: List[ProductData] = []
        soup = BeautifulSoup(page_html, 'html.parser')
        products = soup.select(CSS_SELECTORS['product'])

        products_by_type = self._get_products_by_rank_type(products)

        logger.debug(f"Length Products: {len(products)}")

        if len(products) == 0:
            self._request_executor.set_random_user_agent()

        for product in products:

            product_model = ProductData(
                dt=datetime.now(),
                product_id=self._get_product_id(product),
                keyword=keyword,
                rank_type=self._get_product_rank_type(product, products_by_type),
                rank=self._get_product_rank(product, products_by_type),
                page_number=page_number,
                bestseller_badge=self._is_product_have_bestseller_badge(product),
                amazonchoice_badge=self._is_product_have_amazonchoice_badge(product)
            )

            logger.info(f"Parse product model: {product_model}")
            product_data_list.append(product_model)

        return product_data_list

    def parse_keyword(self, keyword: str, page_per_keyword: int) -> List[ProductData]:
        """Parse all detailed data for keyword"""
        product_page_list = []

        for page in range(1, page_per_keyword+1):
            logger.debug(f"Parse page: № {page}")
            html_data = self._request_executor.get_search_page_html(keyword=keyword,
                                                                    page=page)
            if html_data:
                page_data = self._extract_page(html_data, keyword=keyword, page_number=page)
                product_page_list.append(page_data)

        return list(itertools.chain(*product_page_list))


    def set_location(self, zip_code: str):
        """Set a location to parsing"""
        return self._request_executor.set_location(zip_code=zip_code)


    def _is_product_have_bestseller_badge(self, product: Tag) -> bool:
        """Return true if product have bestseller badge"""

        badge = self._get_badge_id_string(product)
        try:
            return badge['badgeType'] == 'best-seller'
        except TypeError:
            return False

    def _is_product_have_amazonchoice_badge(self, product) -> bool:
        """Return true if product have amazon choice badge"""

        badge = self._get_badge_id_string(product)
        try:
            return badge['badgeType'] == 'amazons-choice'
        except TypeError:
            return False

    def _get_product_id(self, product: ResultSet) -> Optional[str]:
        """Return a product id from product url"""
        product_url_select = product.select(CSS_SELECTORS['url'])
        if not product_url_select:
            return None

        url = product_url_select[0].get('href')
        logger.info(f'Url: {url}')

        if 'slredirect' in url:
            url = self._request_executor.get_normal_url(url)

        product_id = url.split("/")[-2]
        logger.info(f"Get product id: {product_id}")
        return product_id

    @staticmethod
    def _get_product_rank(product: Tag, products_by_type: collections.defaultdict):
        """Get rank of product"""

        if product in products_by_type['sponsored']:
            # Get index of element from list. It will be a rank
            return products_by_type['sponsored'].index(product) + 1

        else:
            return products_by_type['organic'].index(product) + 1

    @staticmethod
    def _get_product_rank_type(product: Tag, products_by_type: collections.defaultdict) -> str:
        """Return rank type of the product"""

        if product in products_by_type['sponsored']:
            return 'sponsored'
        else:
            return 'organic'

    @staticmethod
    def _get_badge_id_string(product: Tag) -> Optional[dict]:
        """Return a string with badge"""

        badge = product.select_one(CSS_SELECTORS['badge'])
        if badge:
            return json.loads(badge.get('data-component-props'))

        return None

    @staticmethod
    def _get_products_by_rank_type(product_list: ResultSet) -> collections.defaultdict:
        """Get products by type"""

        data = collections.defaultdict(list)

        for product in product_list:
            if 'AdHolder' in product.get('class'):
                data['sponsored'].append(product)
            else:
                data['organic'].append(product)

        return data

