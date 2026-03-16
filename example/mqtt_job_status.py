"""
示例：MQTT 连接与作业状态监听
=============================

展示如何通过 MQTT 订阅 RenderG 消息队列，实时监听当前用户下
所有作业及子任务的状态变更通知。

运行前提：
    - config.json 中已配置 AUTH_KEY、CLUSTER_ID

运行方式：
    python example/mqtt_job_status.py

流程：
    1. 初始化 RenderGAPI
    2. 调用 api.user.get_user_info() 获取 user_id
    3. 建立 MQTT 连接（MqttClient）
    4. 订阅主题 mqtt/renderg/status/{user_id}，
       接收该用户下所有作业的状态变更消息
    5. 阻塞等待消息，Ctrl+C 后取消订阅并退出

消息类型（type_id）说明：
    010008  作业状态变更（job_id 在消息根层级，新旧状态在 data 中）
    010007  子任务状态变更（job_id 在消息根层级，层标识和新旧状态在 data 中）
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.MQClient import MqttClient
from renderg_utils import utils, log

config = utils.read_json("../config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()

api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

user_id = api.user.get_user_info().get("user_id")
if not user_id:
    logger.error("无法获取 user_id，请检查 AUTH_KEY 是否正确")
    sys.exit(1)

auth_key = api.mqConnect.get_key()
user_name = "{}_{}_sdk".format(user_id, int(time.time()))

mqtt_client = MqttClient(user_name, auth_key)

topic = "mqtt/renderg/status/{}".format(user_id)
logger.info("准备订阅主题：{}".format(topic))

received = [] # 用于存储收到的消息，方便后续处理或统计
def on_job_status(raw):
    """
    MQTT 消息回调函数。

    Args:
        raw (str): 收到的原始消息（JSON 字符串）。
    """
    logger.info("收到消息：{}".format(raw))

    try:
        payload = json.loads(raw)
    except ValueError:
        logger.warning("消息非 JSON 格式，跳过处理")
        return

    type_id = payload.get("type_id", "")
    data    = payload.get("data", {})
    job_id = payload.get("job_id", "")

    if str(type_id) == "010008":

        old_status = data.get("old_Status", "")
        new_status = data.get("Status", "")
        logger.info("作业状态变更通知：job_id={}, old_status={}, new_status={}".format(job_id, old_status, new_status))
    elif str(type_id) == "010007":
        layer = data.get("identification", "")
        old_status = data.get("old_status", "")
        new_status = data.get("new_status", "")
        logger.info("子任务状态变更通知：job_id={}, layer={}, old_status={}, new_status={}".format(
            job_id, layer, old_status, new_status
        ))
    else:
        logger.info("收到未处理的事件类型 type_id={}，data={}".format(
            type_id, json.dumps(data, ensure_ascii=False)
        ))

    received.append(payload)

mqtt_client.subscribe(topic, on_job_status)
logger.info("订阅成功，等待作业状态消息（按 Ctrl+C 退出）...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("收到退出信号，正在取消订阅...")
    mqtt_client.unsubscribe(topic)
    logger.info("已退出。本次共收到 {} 条消息。".format(len(received)))
