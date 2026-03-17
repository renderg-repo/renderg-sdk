example
==========

example 包包含 RenderG SDK 的使用示例，展示了如何使用 SDK 与 RenderG 渲染服务进行交互。

该包提供了以下主要示例：

- **submit_clarisse.py**: Clarisse 场景文件的渲染提交示例
- **submit_houdini.py**: Houdini 场景文件的渲染提交示例
- **submit_maya.py**: Maya 场景文件的渲染提交示例
- **mqtt_job_status.py**: MQTT 连接与作业状态实时监听示例

这些示例展示了完整的渲染工作流，包括：
- 初始化 RenderG API 连接
- 分析 DCC 文件信息
- 设置渲染参数和层
- 上传场景文件和资源
- 提交渲染作业
- 监控渲染进度
- 下载渲染结果

通过这些示例，用户可以快速了解如何将 RenderG SDK 集成到自己的渲染工作流中。

.. toctree::
   :maxdepth: 2

   example/submit_clarisse
   example/submit_houdini
   example/submit_maya
   example/mqtt_job_status
