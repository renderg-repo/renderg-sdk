.. _analyze_maya_analyze:

analyze_maya.analyze
====================

该模块包含 ``AnalyzeMaya`` 类，负责解析 Maya 场景文件并收集所有依赖资产，
同时在 RenderG 服务器创建渲染作业（Job）记录。

分析完成后，可通过以下属性获取结果：

- ``analyze_obj.info_path`` —— 生成的 ``info.cfg`` 资产清单文件路径，上传时使用
- ``analyze_obj.job_id`` —— 服务器分配的作业 ID

.. automodule:: analyze_maya.analyze
   :members:
   :undoc-members:
   :show-inheritance: