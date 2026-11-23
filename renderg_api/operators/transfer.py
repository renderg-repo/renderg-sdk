import requests

import renderg_utils
from renderg_api.connect import Connect


class TransferOperator(object):
    """
    传输操作符类，提供文件传输相关的配置查询功能。

    该类负责获取 Aspera 文件传输所需的服务器地址、端口、账号凭证等信息，
    供 RenderGUpload 和 RenderGDownload 使用。
    """

    def __init__(self, connect: 'Connect'):
        """
        初始化传输操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def _get_transfer_lines(self):
        """
        获取所有传输线路的原始数据。

        Returns:
            dict: 以集群 ID 为键、线路配置列表为值的字典。
        """
        return self._connect.get(self._connect.urls.GetTransferLine).get('data')

    def get_transfer_line(self, line_id, direction="upload"):
        """
        根据线路 ID 获取对应传输服务器的主机地址和端口。

        Args:
            line_id (int): 传输线路 ID，对应 :class:`~renderg_api.constants.TransferLines` 中的常量，
                           例如 ``TransferLines.LINE_UNICOM`` （联通）、``TransferLines.LINE_TELECOM`` （电信）。
            direction (str, optional): ``"upload"`` 或 ``"download"``，默认 ``"upload"``。
                下载时优先使用线路的 ``transfer_plus_host_down`` / ``transfer_plus_port_down``。

        Returns:
            tuple: ``(host, port)``，分别为传输服务器的主机地址（str）和端口号（int）。
                若启用了定制代理，则返回代理程序的主机地址和映射后的端口。

        Raises:
            TypeError: 当指定的线路 ID 在当前集群中未找到对应的主机或端口时抛出。
        """
        host = ''
        port = 0

        transfer_lines = self._get_transfer_lines()
        lines = transfer_lines.get(str(self._connect.cluster_id))
        if lines:
            for line in lines:
                if line.get("ISP_id") == line_id:
                    host = line.get('transfer_plus_host')
                    port = line.get('transfer_plus_port')
                    if direction == "download":
                        download_host = line.get('transfer_plus_host_down', '')
                        download_port = line.get('transfer_plus_port_down', '')
                        if download_host and download_port:
                            host = download_host
                            port = download_port
        if not host or not port:
            raise TypeError('Required "host" or "port" not specified. host: "{}", port: "{}"'.format(host, port))

        return self._apply_proxy(host, port)

    def get_transfer_config(self, job_id):
        """
        获取指定作业的文件传输凭证配置。

        Args:
            job_id (str): 作业 ID。

        Returns:
            dict: 传输配置字典，包含以下字段：

                - ``username`` (str): 上传用的 Aspera 用户名。
                - ``output_username`` (str): 下载用的 Aspera 用户名。
                - ``password`` (str): Aspera 传输密码。
        """
        params = {'job_id': str(job_id)}
        return self._connect.post(self._connect.urls.GetTransferConfig, params).get('data')

    def get_transfer_cluster(self, cluster_id):
        """
        根据集群 ID 获取该集群的传输配置列表。

        主要用于下载时未指定具体 ``job_id`` 的场景（自定义下载）。

        Args:
            cluster_id (str): 集群 ID。

        Returns:
            list: 传输配置列表，每个元素包含 ``username``、``output_username``、``password`` 等字段。
        """
        params = {'cluster_id': str(cluster_id)}
        data = self._connect.post(self._connect.urls.GetTransferByCluster, params).get('data')
        return data

    def _apply_proxy(self, host, port):
        proxy = getattr(self._connect, "proxy", None)
        if not proxy or not proxy.get("state"):
            return host, port

        proxy_host = proxy.get("host")
        proxy_api_port = proxy.get("api_port")
        if not proxy_host or not proxy_api_port:
            return host, port

        proxy_config = proxy.get("config")
        if not proxy_config:
            proxy_config = self._fetch_proxy_config(proxy_host, proxy_api_port)

        proxy_port = self._get_proxy_port(proxy_config, host, "tcp")
        if proxy_port:
            renderg_utils.get_logger().info(
                "transfer proxy: %s:%s -> %s:%s", host, port, proxy_host, proxy_port
            )
            return proxy_host, proxy_port

        renderg_utils.get_logger().warning(
            "proxy config has no tcp mapping for %s, fallback to %s:%s",
            host, proxy_host, port,
        )
        return proxy_host, port

    @staticmethod
    def _fetch_proxy_config(host, api_port, timeout=5):
        url = "http://{}:{}/config".format(host, api_port)
        try:
            response = requests.get(url, timeout=timeout, proxies={})
            response.raise_for_status()
            return response.json()
        except Exception as err:
            renderg_utils.get_logger().warning(
                "get proxy config failed: %s (%s)", url, err
            )
            return {}

    @staticmethod
    def _get_proxy_port(proxy_config, host, protocol="tcp"):
        if not isinstance(proxy_config, dict):
            return None
        for _, item in proxy_config.items():
            if not isinstance(item, dict):
                continue
            if item.get("type") != protocol:
                continue
            local_ips = (
                str(item.get("local_ip", "")).strip().lower(),
                str(item.get("local_lan_ip", "")).strip().lower(),
            )
            if str(host).strip().lower() in local_ips:
                try:
                    return int(item.get("remote_port"))
                except (TypeError, ValueError):
                    return None
        return None
