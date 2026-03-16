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

    def get_transfer_line(self, line_id):
        """
        根据线路 ID 获取对应传输服务器的主机地址和端口。

        Args:
            line_id (int): 传输线路 ID，对应 :class:`~renderg_api.constants.TransferLines` 中的常量，
                           例如 ``TransferLines.LINE_UNICOM`` （联通）、``TransferLines.LINE_TELECOM`` （电信）。

        Returns:
            tuple: ``(host, port)``，分别为传输服务器的主机地址（str）和端口号（int）。

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
        if not host or not port:
            raise TypeError('Required "host" or "port" not specified. host: "{}", port: "{}"'.format(host, port))
        return host, port

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
