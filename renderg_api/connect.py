import copy
import json

import requests
from tenacity import retry
from tenacity import stop_after_attempt, wait_random

from renderg_api.constants import HEADERS
from renderg_api.exception import RenderGAPIError
from renderg_api.urls import assemble_api_url, ApiUrl


class Connect(object):
    """
    与RenderG服务器进行HTTP通信的连接类。
    
    该类负责处理所有与服务器的HTTP请求，包括认证、请求发送、重试机制和错误处理。
    """

    def __init__(self, auth_key, protocol, domain, cluster_id, header=None):
        """
        初始化连接实例。
        
        Args:
            auth_key (str): 用户认证密钥。
            protocol (str): 通信协议（http/https）。
            domain (str): 服务器域名和端口。
            cluster_id (str): 集群ID。
            header (dict, optional): 自定义HTTP请求头。
        """
        self.cluster_id = cluster_id
        self.urls = ApiUrl

        self._auth_key = auth_key
        self.domain = domain
        self._protocol = protocol
        if header:
            HEADERS.update(header)
        self._headers = HEADERS
        self._headers["Authorization"] = auth_key

        self._session = requests.Session()

    @property
    def headers(self):
        """
        获取当前HTTP请求头。
        
        Returns:
            dict: HTTP请求头字典。
        """
        return self._headers

    @retry(reraise=True, stop=stop_after_attempt(5),
           wait=wait_random(min=1, max=2))
    def post(self, api_url, data=None, params=None, validator=True):
        """
        发送POST请求到服务器。
        
        Args:
            api_url (str): API路径。
            data (dict, optional): 请求数据。
            params (dict, optional): URL参数。
            validator (bool, optional): 是否进行数据验证，默认为True。
            
        Returns:
            dict: 服务器响应的JSON数据。
            
        Raises:
            RenderGAPIError: 当服务器返回错误时抛出。
        """
        if not data:
            data = {}

        if validator:
            # todo data validator
            pass

        request_url = assemble_api_url(self.domain, api_url, self._protocol)
        data = json.dumps(data)

        response = self._session.post(request_url, data=data, headers=self._headers, params=params)
        response_json = response.json()

        if not response.ok:
            response_code = response_json.get('error_code')
            raise RenderGAPIError(response_code, response_json.get("msg", ""), response.url)

        return response_json

    @retry(reraise=True, stop=stop_after_attempt(5),
           wait=wait_random(min=1, max=2))
    def get(self, api_url, data=None, params=None, validator=True):
        """
        发送GET请求到服务器。
        
        Args:
            api_url (str): API路径。
            data (dict, optional): 请求数据。
            params (dict, optional): URL参数。
            validator (bool, optional): 是否进行数据验证，默认为True。
            
        Returns:
            dict: 服务器响应的JSON数据。
            
        Raises:
            RenderGAPIError: 当服务器返回错误时抛出。
        """
        if not data:
            data = {}

        if validator:
            # todo data validator
            pass

        request_url = assemble_api_url(self.domain, api_url, self._protocol)
        data = json.dumps(data)

        response = self._session.get(request_url, data=data, headers=self._headers, params=params)
        response_json = response.json()

        if not response.ok:
            response_code = response_json.get('error_code')
            raise RenderGAPIError(response_code, response_json.get("msg", ""), response.url)

        return response_json
