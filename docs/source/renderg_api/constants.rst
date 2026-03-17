renderg_api.constants
==========================

该模块定义了 SDK 中使用的公共常量类。

**ControlType** — 作业/任务控制操作类型

.. code-block:: python

   from renderg_api.constants import ControlType

   # 可用常量：START / STOP / DELETE / SUSPEND / SPEEDUP / REQUEUE

**TransferLines** — 文件传输线路

.. code-block:: python

   from renderg_api.constants import TransferLines

   TransferLines.LINE_RENDERG   # 内网专线
   TransferLines.LINE_UNICOM    # 中国联通
   TransferLines.LINE_TELECOM   # 中国电信

**JobStatus** — 作业状态码

.. code-block:: python

   from renderg_api.constants import JobStatus

   JobStatus.STATUS_ANALYZE_DOING    # 分析中
   JobStatus.STATUS_ANALYZED         # 分析完成
   JobStatus.STATUS_UPLOAD           # 上传中
   JobStatus.STATUS_ANALYZE_FAILED   # 分析失败
   JobStatus.STATUS_COMPLETED        # 渲染完成

.. automodule:: renderg_api.constants
   :members:
   :undoc-members:
   :show-inheritance:
