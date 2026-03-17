.. _analyze_clarisse_analyze:

analyze_clarisse.analyze
========================

该模块包含 ``AnalyzeClarisse`` 类，负责解析 Clarisse iFX 场景文件（``.project``）并收集所有依赖资产，
同时在 RenderG 服务器创建渲染作业记录。

分析完成后，可通过以下属性获取结果：

- ``analyze_obj.info_path`` —— 生成的 ``info.cfg`` 资产清单文件路径，上传时使用
- ``analyze_obj.job_id`` —— 服务器分配的作业 ID

.. automodule:: analyze_clarisse.analyze
   :members:
   :undoc-members:
   :show-inheritance: