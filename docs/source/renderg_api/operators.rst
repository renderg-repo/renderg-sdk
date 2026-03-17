renderg_api.operators
========================

Operator 模块封装了针对不同资源的 API 操作，所有 Operator 实例均通过
:class:`~renderg_api.core.RenderGAPI` 的属性访问，无需手动创建。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 类
     - 访问方式
     - 说明
   * - :class:`~renderg_api.operators.config.ConfigOperator`
     - ``api.config``
     - 查询集群列表和区域（Zone）硬件配置
   * - :class:`~renderg_api.operators.env.EnvOperator`
     - ``api.env``
     - 查询渲染环境，获取 DCC 软件版本、插件配置等信息
   * - :class:`~renderg_api.operators.job.JobOperator`
     - ``api.job``
     - 创建、提交、控制（开始/停止/加速/重新排队）、查询渲染作业
   * - :class:`~renderg_api.operators.project.ProjectOperator`
     - ``api.project``
     - 查询用户的渲染项目列表
   * - :class:`~renderg_api.operators.task.TaskOperator`
     - ``api.task``
     - 控制和查询作业内的帧任务（Task）
   * - :class:`~renderg_api.operators.transfer.TransferOperator`
     - ``api.transfer``
     - 获取文件传输服务器地址、端口及凭证
   * - :class:`~renderg_api.operators.user.UserOperator`
     - ``api.user``
     - 查询用户可用的集群和区域列表

.. toctree::
   :maxdepth: 2

   operators/config
   operators/env
   operators/job
   operators/project
   operators/task
   operators/transfer
   operators/user

.. automodule:: renderg_api.operators
   :members:
   :undoc-members:
   :show-inheritance:
