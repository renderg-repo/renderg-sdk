
class UserOperator(object):
    """
    用户操作符类，提供与用户账户相关的查询功能。
    """

    def __init__(self, connect):
        """
        初始化用户操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def get_user_info(self):
        """
        获取当前用户的账户信息。

        Returns:
            dict: 包含用户账户信息的字典

        Examples:
            >>> api.user.get_user_info()
            {}
        """
        response = self._connect.get(self._connect.urls.GetUserInfo)
        return response

    def get_cluster_list(self):
        """
        获取当前用户可用的集群列表。

        Returns:
            list: 集群信息列表，每个元素为包含集群详情的字典。
                  若无可用集群则返回空列表。

        Examples:
            >>> api.user.get_cluster_list()
            [
                {
                    "busyness": 1,
                    "description": "支持CPU渲染",
                    "id": 43,
                    "name": "西北一区",
                    "thumb_url": null,
                    "velocities": [
                        {
                            "desc": "电信",
                            "download_host": null,
                            "download_url": null,
                            "id": 1102,
                            "index": 3,
                            "name": "电信",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        },
                        {
                            "desc": "联通",
                            "download_host": null,
                            "download_url": null,
                            "id": 1101,
                            "index": 2,
                            "name": "联通",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        },
                        {
                            "desc": "移动",
                            "download_host": null,
                            "download_url": null,
                            "id": 1183,
                            "index": 1,
                            "name": "移动",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        }
                    ]
                },
                {
                    "busyness": 1,
                    "description": "支持CPU渲染",
                    "id": 47,
                    "name": "CPU六区",
                    "thumb_url": null,
                    "velocities": [
                        {
                            "desc": "电信",
                            "download_host": null,
                            "download_url": null,
                            "id": 1117,
                            "index": 3,
                            "name": "电信",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        },
                        {
                            "desc": "联通",
                            "download_host": null,
                            "download_url": null,
                            "id": 1116,
                            "index": 2,
                            "name": "联通",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        },
                        {
                            "desc": "移动",
                            "download_host": null,
                            "download_url": null,
                            "id": 1173,
                            "index": 1,
                            "name": "移动",
                            "transfer_plus_host": "218.202.112.57",
                            "upload_host": null,
                            "upload_url": null
                        }
                    ]
                },
                ...
            ]
        """
        response = self._connect.get(self._connect.urls.GetClusterList)
        return response.get("collection", [])

    def get_zone_list(self):
        """
        获取可用的区域（Zone）配置列表。

        Returns:
            dict: 服务器返回的区域列表响应数据，包含各区域的硬件配置信息（CPU、内存等）。

        Examples:
            >>> api.user.get_zone_list()
            {
                "47": [
                    {
                        "busyness": 0,
                        "description": "56线",
                        "dummy": false,
                        "is_gpu": false,
                        "name": "CPU 28核心/56线程",
                        "ram_limits": [
                            "64G",
                            "128G"
                        ],
                        "zone_id": 1009
                    },
                    {
                        "busyness": 0,
                        "description": "104线",
                        "dummy": false,
                        "is_gpu": false,
                        "name": "CPU 52核心/104线程",
                        "ram_limits": [
                            "64G",
                            "128G",
                            "192G",
                            "256G",
                            "512G"
                        ],
                        "zone_id": 1012
                    }
                ],
                ...
            }
        """
        response = self._connect.get(self._connect.urls.GetZoneList)
        return response
