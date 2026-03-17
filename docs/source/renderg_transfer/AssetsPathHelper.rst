renderg_transfer.AssetsPathHelper
====================================

:class:`~renderg_transfer.AssetsPathHelper.AssetsPathHelper` 负责解析 DCC 分析模块生成的
``info.cfg`` 配置文件，并将其中的本地资产路径转换为 Aspera 传输所需的
``(源路径, 目标路径)`` 列表，供 :class:`~renderg_transfer.RGUpload.RenderGUpload` 使用。

该模块为 SDK 内部工具类，通常不需要直接调用。

.. automodule:: renderg_transfer.AssetsPathHelper
   :members:
   :undoc-members:
   :show-inheritance:
