# coding=utf-8
"""
示例：上传自定义资产到 RenderG 存储
====================================

将本地文件或目录直接上传到 RenderG 存储，不创建渲染作业。
远端路径按本地目录结构自动生成，目录不做遍历。

运行前提：
    - config.json 中已配置 AUTH_KEY、CLUSTER_ID
    - 本地路径存在，且当前网络可访问所选传输线路

运行方式：
    python example/upload_assets.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.RGAssetUpload import RenderGAssetUpload
from renderg_utils import utils, log

if __name__ == "__main__":
    config = utils.read_json("../config.json")
    workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

    log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
    logger = log.get_logger()
    logger.info("SDK Version: {}".format(utils.get_version()))

    api = RenderGAPI(
        auth_key=config["AUTH_KEY"],
        cluster_id=config["CLUSTER_ID"],
        proxy=config.get("PROXY"),
    )

    uploader = RenderGAssetUpload(
        api=api,
        line=TransferLines.LINE_UNICOM,  # 内网 LINE_RENDERG / 联通 LINE_UNICOM / 电信 LINE_TELECOM
        speed=1000,                      # 最大传输速度，单位 Mbps
        workspace=workspace,
    )

    result = uploader.upload([
        "D:/Project/assets",             # 目录：直接写入 pair list，不遍历
        "D:/Project/scene/hero.fbx",     # 文件
    ])

    for local_path, remote_path in result:
        logger.info("{} -> {}".format(local_path, remote_path))
