renderg_transfer
===================

renderg_transfer 是 RenderG SDK 的文件传输包，提供了与 RenderG 渲染服务之间的高效文件传输功能。

该包包含以下主要功能：

- 管理渲染资产的路径和文件列表
- 实现高效的文件上传功能（支持 Aspera 高速传输协议）
- 支持将本地文件/目录直接上传到存储（自定义资产上传）
- 实现渲染结果的下载功能
- 提供传输任务的辅助工具和配置
- 支持与 RenderG 消息队列服务的连接和通信

.. toctree::
   :maxdepth: 2

   renderg_transfer/AssetsPathHelper
   renderg_transfer/MQClient
   renderg_transfer/RGAssetUpload
   renderg_transfer/RGDownload
   renderg_transfer/RGUpload
   renderg_transfer/TransferHelper
