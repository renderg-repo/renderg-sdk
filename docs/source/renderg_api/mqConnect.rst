renderg_api.mqConnect
==========================

:class:`~renderg_api.mqConnect.MqConnect` 是消息队列凭证的持有者，
由 :class:`~renderg_api.core.RenderGAPI` 在初始化时创建（``api.mqConnect``）。

其主要用途是向 :class:`~renderg_transfer.MQClient.MqttClient` 提供 MQTT 连接所需的认证密钥，
使下载模块能够订阅作业完成通知，开发者通常不需要直接使用本模块。

.. automodule:: renderg_api.mqConnect
   :members:
   :undoc-members:
   :show-inheritance:
