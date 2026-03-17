.. RenderGSDK documentation master file, created by
   sphinx-quickstart on Fri Nov 14 15:07:15 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RenderGSDK's documentation!
======================================

RenderG SDK 是面向 RenderG 云渲染平台的 Python 客户端开发工具包，帮助开发者将 DCC 软件（Maya、Houdini、Clarisse 等）
的渲染工作流快速接入 RenderG 渲染农场。

**主要功能**

- 提交和管理渲染作业（Job/Task 生命周期控制）
- 分析 DCC 场景文件，自动收集依赖资产清单
- 使用 Aspera 高速协议上传场景文件和资产
- 等待渲染完成后自动下载渲染结果
- 通过 MQTT 实时监听作业状态变更

**快速开始**

1. 安装 SDK::

      pip install renderg-sdk

2. 准备配置文件 ``config.json``::

      {
        "AUTH_KEY": "your_auth_key",
        "CLUSTER_ID": your_cluster_id,
        "ZONE_ID": your_zone_id,
        "RAM_LIMIT": "your_ram_limit",
      }

3. 初始化 API 并提交渲染作业::

      from renderg_api import RenderGAPI

      api = RenderGAPI(auth_key="your_auth_key", cluster_id=27)

   完整的提交流程请参考 :doc:`example` 中各 DCC 软件的示例脚本。

----

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   renderg_api
   renderg_transfer
   renderg_utils
   analyze_clarisse
   analyze_houdini
   analyze_maya
   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
