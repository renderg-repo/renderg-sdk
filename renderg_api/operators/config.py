
class ConfigOperator(object):
    """
    配置操作符类，提供集群和区域（Zone）硬件配置的查询功能。
    """

    def __init__(self, connect):
        """
        初始化配置操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def get_cluster_list(self):
        """
        获取所有可用的集群列表及其详细信息。

        Returns:
            dict: 服务器返回的集群列表响应数据，包含各集群的 ID、名称、状态等信息。
        """
        response = self._connect.get(self._connect.urls.GetClusterList)
        return response

    def get_zone_list(self, cluster_id=""):
        """
        获取可用的区域（Zone）硬件配置列表。

        区域（Zone）定义了渲染节点的硬件规格，例如 CPU 型号、核心数等，
        在提交作业时通过 ``zone_id`` 参数指定。

        Args:
            cluster_id (str, optional): 集群 ID，用于筛选指定集群下的区域列表。
                                         留空则返回所有集群的区域配置。

        Returns:
            dict: 服务器返回的区域列表响应数据，包含各区域的 ID、名称、
                  CPU 配置、内存配置等信息。
        """
        params = {}
        if cluster_id:
            params = {
                'cluster_id': cluster_id
            }
        response = self._connect.get(self._connect.urls.GetZoneList, params)
        return response