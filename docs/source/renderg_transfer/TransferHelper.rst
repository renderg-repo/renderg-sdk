renderg_transfer.TransferHelper
==================================

:class:`~renderg_transfer.TransferHelper.TransferHelper` 提供构建 Aspera ``ascp`` 命令行
所需的静态工具方法，包括生成文件对列表文件（``--file-pair-list``）和拼接完整命令字符串。

:class:`~renderg_transfer.TransferHelper.TransferConstants` 定义了 ``info.cfg``
配置文件中各字段的 key 常量，供 :class:`~renderg_transfer.AssetsPathHelper.AssetsPathHelper`
解析时使用。

以上均为 SDK 内部工具类，通常不需要直接调用。

.. automodule:: renderg_transfer.TransferHelper
   :members:
   :undoc-members:
   :show-inheritance:
