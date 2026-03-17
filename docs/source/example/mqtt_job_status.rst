mqtt_job_status.py
==================

本示例展示如何通过 MQTT 订阅 RenderG 消息队列，实时监听当前用户下所有作业及子任务的状态变更通知。

**前置条件**

- ``config.json`` 中已配置 ``AUTH_KEY``、``CLUSTER_ID``
- 无需指定 ``JOB_ID``，订阅主题覆盖该账号下的所有作业

**流程说明**

1. **初始化 API** —— 从 ``config.json`` 读取认证信息，实例化 :class:`~renderg_api.core.RenderGAPI`
2. **获取 user_id** —— 调用 ``api.user.get_user_info()`` 获取当前用户 ID，
   用于构造 MQTT 主题和客户端标识；若获取失败则立即退出
3. **建立 MQTT 连接** —— 以 ``{user_id}_{timestamp}_sdk`` 为客户端 ID、
   ``auth_key`` 为密码，实例化 :class:`~renderg_transfer.MQClient.MqttClient`；
   连接建立后自动启动后台接收线程
4. **订阅状态主题** —— 订阅 ``mqtt/renderg/status/{user_id}``，
   该主题推送此账号下所有作业的状态变更消息
5. **阻塞监听** —— 主线程循环等待，消息由后台线程接收并分发到 ``on_job_status`` 回调
6. **退出** —— 按 ``Ctrl+C`` 后取消订阅、打印收到消息总数并退出

**消息格式**

所有消息均为 JSON 字符串，``job_id`` 位于消息根层级，事件相关字段位于 ``data`` 对象中。

*作业状态变更* （``type_id = "010008"``）：

.. code-block:: json

   {
     "type_id": "010008",
     "job_id": "123456",
     "data": {
       "old_Status": "RENDERING",
       "Status": "COMPLETED"
     }
   }

*子任务状态变更* （``type_id = "010007"``）：

.. code-block:: json

   {
     "type_id": "010007",
     "job_id": "123456",
     "data": {
       "identification": "defaultRenderLayer",
       "old_status": "RENDERING",
       "new_status": "COMPLETED"
     }
   }

**消息类型对照表**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - type_id
     - 事件
     - data 字段说明
   * - ``010008``
     - 作业状态变更
     - ``old_Status`` 原状态，``Status`` 新状态
   * - ``010007``
     - 子任务状态变更
     - ``identification`` 层名称，``old_status`` 原状态，``new_status`` 新状态

**完整代码**

.. literalinclude:: ../../../example/mqtt_job_status.py
   :language: python
   :linenos:
