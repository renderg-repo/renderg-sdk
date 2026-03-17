renderg_api.operators.env
==============================

:class:`~renderg_api.operators.env.EnvOperator` 提供渲染环境配置的查询功能，
通过 ``api.env`` 访问。

渲染环境（Environment）定义了 DCC 软件版本、插件版本、项目路径等渲染节点所需的运行时配置，
在 RenderG 客户端的环境管理界面中创建，提交作业时通过 ``env_id`` 指定。

**示例**::

   # 获取所有 Maya 环境
   envs = api.env.get_env_list(software_name="maya")
   for env in envs:
       print(env.get("id"), env.get("software_version"))

   # 根据 ID 获取环境详情（含 project_path、definition 等）
   env_info = api.env.get_env_info_by_id(17877)
   print(env_info.get("project_path"))
   print(env_info.get("definition"))

.. automodule:: renderg_api.operators.env
   :members:
   :undoc-members:
   :show-inheritance:
