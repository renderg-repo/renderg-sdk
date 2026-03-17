submit_maya.py
==============

本示例演示如何使用 RenderG SDK 完整提交一个 Maya 渲染作业，涵盖从场景分析到下载结果的全流程。

**前置条件**

- 已创建 ``config.json``，包含 ``AUTH_KEY``、``CLUSTER_ID``、``ZONE_ID``、``RAM_LIMIT`` 等字段
- 已在 RenderG 客户端中创建好项目（``project_id``）和 Maya 渲染环境（``env_id``）

**流程说明**

1. **读取配置、初始化 API** —— 从 ``config.json`` 中读取认证信息，实例化 :class:`~renderg_api.core.RenderGAPI`
2. **分析场景** —— :class:`~analyze_maya.analyze.AnalyzeMaya` 解析 ``.ma`` 文件，
   收集贴图、代理等依赖资产，生成 ``info.cfg`` 清单，并在服务器创建作业记录（得到 ``job_id``）
3. **设置渲染参数** —— :class:`~analyze_maya.param_check.ParamChecker` 设置渲染层、帧范围、
   摄像机、分辨率、硬件配置（``zone_id``、``ram_limit``）等
4. **上传资产** —— :class:`~renderg_transfer.RGUpload.RenderGUpload` 通过 Aspera 协议上传本地文件
5. **提交作业** —— 调用 ``api.job.submit_job(job_id)`` 正式开始渲染
6. **自动下载** —— :class:`~renderg_transfer.RGDownload.RenderGDownload` 通过 MQTT 监听作业完成，
   渲染结束后自动下载结果文件到本地

**完整代码**

.. literalinclude:: ../../../example/submit_maya.py
   :language: python
   :linenos:
