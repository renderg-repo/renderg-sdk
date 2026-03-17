renderg_api.exception
=========================

当 HTTP 请求返回非 2xx 状态码时，:class:`~renderg_api.connect.Connect`
会抛出 :class:`~renderg_api.exception.RenderGAPIError` 异常。

**捕获示例**::

   from renderg_api import RenderGAPI
   from renderg_api.exception import RenderGAPIError

   api = RenderGAPI(auth_key="your_auth_key", cluster_id=27)

   try:
       api.job.submit_job(job_id=999999)
   except RenderGAPIError as e:
       print(e.err_code)      # 业务错误码
       print(e.err_msg)       # 错误描述
       print(e.request_url)   # 触发异常的请求 URL

.. automodule:: renderg_api.exception
   :members:
   :undoc-members:
   :show-inheritance:
