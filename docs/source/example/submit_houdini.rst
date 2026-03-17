submit_houdini.py
=================

本示例演示如何使用 RenderG SDK 完整提交一个 Houdini 渲染作业，涵盖从场景分析到下载结果的全流程。

**前置条件**

- 已创建 ``config.json``，包含 ``AUTH_KEY``、``CLUSTER_ID``、``ZONE_ID``、``RAM_LIMIT`` 等字段
- 已在 RenderG 客户端中创建好项目（``project_id``）和 Houdini 渲染环境（``env_id``）

**流程说明**

1. **读取配置、初始化 API** —— 从 ``config.json`` 中读取认证信息，实例化 :class:`~renderg_api.core.RenderGAPI`
2. **分析场景** —— :class:`~analyze_houdini.analyze.AnalyzeHoudini` 解析 ``.hip`` 文件，
   收集依赖资产，生成 ``info.cfg`` 清单，并在服务器创建作业记录（得到 ``job_id``）
3. **设置渲染参数** —— :class:`~analyze_houdini.param_check.ParamChecker` 通过
   ``set_render_nodes`` 指定 ROP 节点（如 ``/out/mantra1``）及帧范围，设置硬件配置
4. **上传资产** —— :class:`~renderg_transfer.RGUpload.RenderGUpload` 通过 Aspera 协议上传本地文件
5. **提交作业** —— 调用 ``api.job.submit_job(job_id)`` 正式开始渲染
6. **自动下载** —— :class:`~renderg_transfer.RGDownload.RenderGDownload` 通过 MQTT 监听作业完成，
   渲染结束后自动下载结果文件到本地

.. tip::

   示例末尾注释中还包含 **自定义下载** 的用法：当 ``job_id=None`` 时，
   可通过 ``custom_download(server_path)`` 手动指定服务器路径下载历史结果。

**完整代码**

.. literalinclude:: ../../../example/submit_houdini.py
   :language: python
   :linenos:
