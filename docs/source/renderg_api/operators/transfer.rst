renderg_api.operators.transfer
====================================

:class:`~renderg_api.operators.transfer.TransferOperator` 提供文件传输相关的配置查询，
通过 ``api.transfer`` 访问。该模块由
:class:`~renderg_transfer.RGUpload.RenderGUpload` 和
:class:`~renderg_transfer.RGDownload.RenderGDownload` 在内部调用，
开发者通常无需直接使用。

主要功能：

- :meth:`~renderg_api.operators.transfer.TransferOperator.get_transfer_line` —— 根据线路 ID 获取 Aspera 服务器地址和端口
- :meth:`~renderg_api.operators.transfer.TransferOperator.get_transfer_config` —— 获取指定作业的上传/下载 Aspera 账号凭证
- :meth:`~renderg_api.operators.transfer.TransferOperator.get_transfer_cluster` —— 按集群获取传输配置（用于自定义下载场景）

.. automodule:: renderg_api.operators.transfer
   :members:
   :undoc-members:
   :show-inheritance:
