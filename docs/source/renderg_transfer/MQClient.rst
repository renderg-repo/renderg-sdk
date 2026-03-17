renderg_transfer.MQClient
============================

:class:`~renderg_transfer.MQClient.MqttClient` 是基于 ``paho-mqtt`` 的 MQTT 客户端封装，
采用单例模式管理连接，用于订阅 RenderG 平台推送的作业状态变更消息。

主要用途是配合 :class:`~renderg_transfer.RGDownload.RenderGDownload` 的
:meth:`~renderg_transfer.RGDownload.RenderGDownload.auto_download_after_job_completed`
方法，实时感知作业完成（``type_id: 030003``）事件。

该模块为 SDK 内部工具类，通常不需要直接调用。

.. automodule:: renderg_transfer.MQClient
   :members:
   :undoc-members:
   :show-inheritance:
