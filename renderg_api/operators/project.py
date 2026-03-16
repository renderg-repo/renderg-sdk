
class ProjectOperator(object):
    """
    项目操作符类，提供渲染项目的查询功能。
    """

    def __init__(self, connect):
        """
        初始化项目操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def get_project_list(self):
        """
        获取当前用户的所有项目列表。

        Returns:
            list: 项目信息列表，每个元素为包含项目详情的字典，
                  通常包含项目 ID、项目名称等字段。

        Examples:
            >>> api.project.get_project_list()
            [
                {
                    "proj_id": 21478,
                    "proj_name": "888",
                    "user_id": 2352
                },
                ...
            ]
        """
        response = self._connect.get(self._connect.urls.GetProjectList)
        return response.get("data")
