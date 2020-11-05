import requests
import time

from typing import Optional
from loguru import logger
from src.amazon_parser.utils import generate_random_useragent

# Constants
BASE_URL = "https://www.amazon.com"
REQUESTS_ATTEMPT_MAX = 3


class RequestExecutor:
    """Amazon request executor from the mobile site view"""

    def __init__(self, request_timeout: int, proxy: str = None):
        """Init client
        :proxy - HTTP proxy in format LOGIN:PASSWORD@IP:PORT"""

        self.session = requests.session()
        self.headers = {
            'Host': 'www.amazon.com',
            'Accept': 'text/html,application/xhtml+xml,\
                      application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }

        if proxy:
            self.session.proxies = {'https': 'http://' + proxy,
                                    'http': 'http://' + proxy}

        self.request_timeout = request_timeout
        self.set_random_user_agent()

    def set_random_user_agent(self):
        """Set a random user agent to session headers"""

        self.headers['user-agent'] = generate_random_useragent()

    @staticmethod
    def _is_page_valid(response: requests.models.Response):
        """Check if page is valid"""

        if response.status_code not in (200, 201):
            return False

        if 'Robot Check' in response.text:
            return False

        return True

    def _make_request(self, url: str, params: dict = None,
                      adt_headers: dict = None, method: str = 'GET') -> Optional[requests.models.Response]:
        """Make a request to url"""

        attempt = 0
        if params is None:
            params = {}

        # Add additional headers if they are needed for the request
        if adt_headers is None:
            adt_headers = {}

        headers = self.headers.copy()
        headers.update(adt_headers)

        while attempt < REQUESTS_ATTEMPT_MAX:
            logger.debug(f"Send a {method} request to URL: {url}, with params: {params}, "
                         f"headers: {adt_headers}, attempt: {attempt}")
            try:
                if method == 'GET':
                    response = self.session.get(url, timeout=30, headers=headers,
                                                params=params)
                else:
                    response = self.session.post(url, timeout=30, headers=headers,
                                                 data=params)

                #logger.debug(response.text)

                logger.debug(f"Request status code: {response.status_code}, "
                             f"response url: {response.url}, response cookies:"
                             f"{response.cookies}")

                if self._is_page_valid(response) is False:
                    continue

                return response

            except requests.exceptions.ReadTimeout:
                logger.error('Timeout error getting a page')

            except requests.exceptions.SSLError:
                logger.error("SSL error while getting a page")

            finally:
                attempt += 1
                time.sleep(self.request_timeout)

            self.set_random_user_agent()

        return None

    def set_location(self, zip_code: str):
        """Set a location """
        url = BASE_URL + '/gp/delivery/ajax/address-change.html'

        data = {'locationType': 'LOCATION_INPUT',
                'zipCode': zip_code,
                'storeContext': 'wireless',
                'deviceType': 'mobileWeb',
                'pageType': 'Gateway'
                }

        headers = {'x-requested-with': 'XMLHttpRequest',
                   'ect': '4g',
                   'downlink': '10'}

        # First of all get request to main page to get cookies
        self._make_request(BASE_URL, method='GET')

        return self._make_request(url, params=data,
                                  adt_headers=headers, method='POST').text

    def get_normal_url(self, redirect_url: str):
        """Get a normal url from reditrct url"""

        return self._make_request(BASE_URL + redirect_url).url

    def get_search_page_html(self, keyword: str, page: int, category: str = None) -> Optional[str]:
        """Get products from the search page"""
        url = BASE_URL + '/s'

        params = {
            'k': keyword,
            'page': page
        }

        if category:
            params['i'] = category

        return self._make_request(url, params=params, method='GET').text
