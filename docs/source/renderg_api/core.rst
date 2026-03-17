renderg_api.core
=====================

:class:`~renderg_api.core.RenderGAPI` 是 SDK 的统一入口类，所有功能均通过其属性访问。

初始化时需提供用户认证密钥 ``auth_key``（可通过环境变量 ``RENDERG_AUTH_KEY`` 传入），
完成后可通过以下属性访问各功能模块：

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 属性
     - 说明
   * - ``api.user``
     - :class:`~renderg_api.operators.user.UserOperator` —— 查询集群、区域列表
   * - ``api.job``
     - :class:`~renderg_api.operators.job.JobOperator` —— 创建、提交、控制渲染作业
   * - ``api.task``
     - :class:`~renderg_api.operators.task.TaskOperator` —— 控制和查询帧任务
   * - ``api.project``
     - :class:`~renderg_api.operators.project.ProjectOperator` —— 查询项目列表
   * - ``api.env``
     - :class:`~renderg_api.operators.env.EnvOperator` —— 查询渲染环境配置
   * - ``api.config``
     - :class:`~renderg_api.operators.config.ConfigOperator` —— 查询集群和区域硬件配置
   * - ``api.transfer``
     - :class:`~renderg_api.operators.transfer.TransferOperator` —— 获取文件传输凭证

**示例**::

   from renderg_api import RenderGAPI

   api = RenderGAPI(auth_key="your_auth_key", cluster_id=27)

   # 查看可用项目
   projects = api.project.get_project_list()

   # 查看 Maya 环境列表
   envs = api.env.get_env_list(software_name="maya")

.. automodule:: renderg_api.core
   :members:
   :undoc-members:
   :show-inheritance:
