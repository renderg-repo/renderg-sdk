renderg_api.urls
=====================

该模块定义了所有 RenderG REST API 的路径枚举 :class:`~renderg_api.urls.ApiUrl`，
以及将域名、路径、协议拼接为完整 URL 的辅助函数 :func:`~renderg_api.urls.assemble_api_url`。

各 Operator 类在内部通过 ``self._connect.urls.Xxx`` 引用这些枚举值，
开发者通常不需要直接使用本模块。

.. automodule:: renderg_api.urls
   :members:
   :undoc-members:
   :show-inheritance:
