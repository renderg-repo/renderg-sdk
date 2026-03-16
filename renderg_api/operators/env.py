import json


class EnvOperator(object):
    """
    环境操作符类，提供渲染环境配置的查询功能。

    渲染环境定义了 DCC 软件版本、插件配置、项目路径等渲染所需的运行时信息，
    可在 RenderG 客户端的环境管理界面中创建和维护。
    """

    def __init__(self, connect):
        """
        初始化环境操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def get_env_list(self, software_name="", software_version=""):
        """
        获取可用的渲染环境列表，支持按软件名称和版本过滤。

        Args:
            software_name (str, optional): DCC 软件名称，例如 ``"maya"``、``"houdini"``。
                                           留空则返回所有软件的环境。
            software_version (str, optional): DCC 软件版本号，例如 ``"2025"``、``"20.5"``。
                                               留空则不按版本过滤。

        Returns:
            list: 环境信息列表，每个元素为包含以下字段的字典：

                - ``id`` (int): 环境 ID。
                - ``software_name`` (str): DCC 软件名称。
                - ``software_version`` (str): DCC 软件版本。
                - ``project_path`` (str): 项目路径。
                - ``definition`` (str): JSON 格式的环境定义（插件、渲染器等配置）。
                - ``extra_info`` (str): JSON 格式的额外配置信息。

        Examples:
            >>> api.env.get_env_list()
            [
                {
                    "created_at": "2023-12-07T10:44:46Z",
                    "created_by": 2352,
                    "definition": "[{\"mtoa\": \"4.2.1.1\"}]",
                    "extra_info": "{\"layer_mode\": \"Render Layer\", \"renderSetup_includeAllLights\": false}",
                    "id": 12016,
                    "name": "2018",
                    "project_path": "E:/Work/Scene/Maya",
                    "retired_at": null,
                    "retired_by": null,
                    "software_name": "maya",
                    "software_version": "2018",
                    "updated_at": "2025-08-11T15:36:00Z",
                    "updated_by": 2352,
                    "user_id": 2352
                },
                ...
            ]
        """
        params = {
            'software_name': software_name,
            'software_version': software_version
        }
        response = self._connect.post(self._connect.urls.GetEnvList, params)
        return response.get("data")

    def get_env_info_by_id(self, env_id):
        """
        根据环境 ID 获取指定环境的详细信息。

        Args:
            env_id (int): 环境 ID，可通过 :meth:`get_env_list` 获取。

        Returns:
            dict: 环境详细信息字典，包含以下字段：

                - ``software_name`` (str): DCC 软件名称。
                - ``software_version`` (str): DCC 软件版本。
                - ``project_path`` (str): 项目路径。
                - ``definition`` (dict): 解析后的环境定义（插件、渲染器等配置）。
                - ``extra_info`` (dict): 解析后的额外配置信息。

            若未找到对应 ID 的环境，则返回空字典 ``{}``。

        Examples:
            >>> env_id = 5335
            >>> api.env.get_env_info_by_id(env_id)
            {
                "software_name": "clarisse_ifx",
                "software_version": "5.0 SP11",
                "project_path": null,
                "definition": [],
                "extra_info": {}
            }
        """
        for env_item in self.get_env_list():
            if env_item.get("id") == env_id:
                definition = json.loads(env_item.get('definition'))
                environment_info = {
                    'software_name': env_item.get('software_name'),
                    'software_version': env_item.get('software_version'),
                    'project_path': env_item.get('project_path'),
                    'definition': definition,
                    'extra_info': json.loads(env_item.get('extra_info')) if env_item.get('extra_info') else {}
                }
                return environment_info

        return {}
