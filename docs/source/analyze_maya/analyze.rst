.. _analyze_maya_analyze:

analyze_maya.analyze
====================

该模块包含 ``AnalyzeMaya`` 类，负责解析 Maya 场景文件并收集所有依赖资产。
默认情况下会同时在 RenderG 服务器创建渲染作业记录（``job_id``）；
也可通过 ``auto_create_job=False`` 将任务号申请推迟到分析完成后再进行。

分析完成后，可通过以下属性获取结果：

- ``analyze_obj.info_path`` —— 生成的 ``info.cfg`` 资产清单文件路径，上传时使用
- ``analyze_obj.job_id`` —— 服务器分配的作业 ID；若使用 ``auto_create_job=False``，
  需手动赋值后才可进行参数检查与提交

.. note::

   ``auto_create_job`` 默认为 ``True``，与旧版本行为完全一致。
   仅当业务流程需要在分析后再决定是否提交时，才需要传入 ``False``。

.. automodule:: analyze_maya.analyze
   :members:
   :undoc-members:
   :show-inheritance: