renderg_api.connect
========================

:class:`~renderg_api.connect.Connect` 是所有 HTTP 通信的底层实现，由 :class:`~renderg_api.core.RenderGAPI`
在初始化时自动创建，通常无需手动使用。

该类的主要职责：

- 维护 ``Authorization`` 请求头，完成身份认证
- 封装 ``GET`` / ``POST`` 请求，并在失败时自动重试（最多 5 次，随机等待 1–2 秒）
- 收到非 2xx 响应时，抛出 :class:`~renderg_api.exception.RenderGAPIError` 异常

.. automodule:: renderg_api.connect
   :members:
   :undoc-members:
   :show-inheritance:
