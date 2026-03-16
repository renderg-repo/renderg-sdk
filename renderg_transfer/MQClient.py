import time

import paho.mqtt.client as mqtt
import renderg_utils

logger = renderg_utils.get_logger()


class MqttClient:
    """
    MQTT 客户端类，用于订阅 RenderG 消息队列以监听作业状态变更通知。

    该类采用单例模式管理底层 MQTT 连接，多次实例化共享同一个连接。
    主要用于 RenderGDownload 中等待作业渲染完成的场景。
    """

    #: paho-mqtt 客户端实例（类变量，单例）。
    client = None
    #: 主题到回调函数的映射字典（类变量）。
    callbacks = {}
    #: MQTT 连接状态码，``0`` 表示连接成功（类变量）。
    rc = None

    def __init__(self, username, password):
        """
        初始化 MQTT 客户端并建立连接（若尚未连接）。

        Args:
            username (str): MQTT 连接用户名，格式通常为 ``{user_id}_{timestamp}_sdk``。
            password (str): MQTT 连接密码（对应 RenderG auth_key）。
        """
        if MqttClient.client is None:
            broker_address = "client.renderg.com"
            port = 1883

            if hasattr(mqtt, "CallbackAPIVersion"):
                MqttClient.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, username)
            else:
                MqttClient.client = mqtt.Client(username)
            MqttClient.client.on_connect = MqttClient.on_connect
            MqttClient.client.on_message = MqttClient.on_message
            if username and password:
                MqttClient.client.username_pw_set(username, password)
            MqttClient.client.connect(broker_address, port)
            MqttClient.client.loop_start()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        """
        MQTT 连接回调，在连接建立或失败时触发。

        Args:
            client: paho-mqtt 客户端实例。
            userdata: 用户数据（未使用）。
            flags: 连接标志（未使用）。
            rc (int): 连接结果码，``0`` 表示成功。
        """
        if rc == 0:
            logger.info("Connected successfully")
        else:
            logger.info("Connection failed with code {rc}".format(rc=rc))
        MqttClient.rc = rc

    @staticmethod
    def on_message(client, userdata, message):
        """
        MQTT 消息接收回调，收到消息时根据主题分发到对应的回调函数。

        Args:
            client: paho-mqtt 客户端实例。
            userdata: 用户数据（未使用）。
            message: 收到的 MQTT 消息对象，包含 ``topic`` 和 ``payload`` 属性。
        """
        topic = message.topic
        payload = message.payload.decode('utf-8')
        if topic in MqttClient.callbacks:
            callback = MqttClient.callbacks[topic]
            callback(payload)

    @staticmethod
    def connect_status():
        """
        获取当前 MQTT 连接状态。

        Returns:
            int or None: 连接结果码，``0`` 表示已连接，``None`` 表示尚未完成连接。
        """
        return MqttClient.rc

    @staticmethod
    def subscribe(topic, callback):
        """
        订阅指定 MQTT 主题，并注册消息回调函数。

        该方法会阻塞等待直到 MQTT 连接建立成功（``rc == 0``）后才执行订阅。

        Args:
            topic (str): 要订阅的 MQTT 主题，例如
                         ``"mqtt/front/user/{user_id}/{job_id}"``。
            callback (callable): 接收到该主题消息时调用的回调函数，接受消息内容（str）作为参数。
        """
        while True:
            if MqttClient.rc == 0:
                logger.info('订阅主题：{topic}'.format(topic=topic))
                MqttClient.client.subscribe(topic, qos=0)
                MqttClient.callbacks[topic] = callback
                break
            else:
                time.sleep(1)

    @staticmethod
    def unsubscribe(topic):
        """
        取消订阅指定 MQTT 主题，并移除对应的回调函数。

        Args:
            topic (str): 要取消订阅的 MQTT 主题。
        """
        if topic in MqttClient.callbacks:
            del MqttClient.callbacks[topic]
            MqttClient.client.unsubscribe(topic)
