
class RenderGAPIError(Exception):
    """
    RenderG API 请求异常类。

    当服务器返回非 2xx 状态码时抛出此异常，包含错误码、错误消息和请求 URL 等信息。

    Attributes:
        err_code (str): 服务器返回的业务错误码。
        err_msg (str): 服务器返回的错误描述信息。
        request_url (str): 触发该异常的请求 URL。

    Example::

        try:
            api.job.submit_job(job_id)
        except RenderGAPIError as e:
            print(e.err_code)   # 错误码
            print(e.err_msg)    # 错误描述
            print(str(e))       # 完整错误信息
    """

    def __init__(self, err_code, err_msg, request_url):
        """
        初始化 API 异常。

        Args:
            err_code (str): 服务器返回的业务错误码。
            err_msg (str): 服务器返回的错误描述信息。
            request_url (str): 触发该异常的请求 URL。
        """
        self.err_code = err_code
        self.err_msg = err_msg
        self.request_url = request_url

    def __str__(self):
        return 'Error code: {}, Error message: {}, URL: {}'.format(
            self.err_code,
            self.err_msg,
            self.request_url
        )
