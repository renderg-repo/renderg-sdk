import os.path

from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.RGDownload import RenderGDownload
from renderg_transfer.RGUpload import RenderGUpload
from renderg_utils import utils, log
from analyze_maya import AnalyzeMaya, ParamChecker

config = utils.read_json("../config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))
api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

# 2. 设置日志模块
log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()
logger.info("SDK Version: {}".format(utils.get_version()))

# 获取环境配置
env_info = api.env.get_env_info_by_id(17877)

analyze_info = {
    "dcc_file": os.path.normpath(r"E:\Work\Scene\Maya\2025.3.ma"),
    "dcc_version": "2025",
    "project_path": env_info.get("project_path") or r"E:\Work\Scene\Maya", # 项目路径， 如果环境中配置了项目路径，可使用环境中的配置，也可重新配置
    "api": api,
    "project_id": 42310,
    "env_id": 17877,
    "workspace": workspace,
    "logger": logger
}
analyze_obj = AnalyzeMaya(**analyze_info)
analyze_obj.analyze()

logger.info(analyze_obj.info_path)

param_check_obj = ParamChecker(api, analyze_obj)
render_params = {
    "ChunkSize": 1,  # 一机多帧
    "Mark": "",  # 任务备注信息
    "task_timeout": 0,  # 任务超时时间，单位分钟，0代表不设置

    "PriorityFrames": "010:",  # 优先渲染帧 例：101:100-108x2 代表渲染首尾帧和100-108步长为2的帧
    "layered_rendering": True,  # 分层渲染，一层一个任务
    "layer_mode": "Render Layer", # 渲染层模式，Render Layer 或 Render Setup, 未设置时使用环境中的配置
    "renderSetup_includeAllLights": False, # render setup 包含所有灯光, 未设置时使用环境中的配置

    "zone_id": config["ZONE_ID"],  # CPU 配置信息
    "ram_limit": config["RAM_LIMIT"],  # 内存配置
}

# 设置要渲染的层，以及相关设置
param_check_obj.set_render_layers({
    "defaultRenderLayer": {
        "ForceRenderFrames": "1-10x2",  # 渲染帧 例：101:100-108x2 代表渲染首尾帧和100-108步长为2的帧
        "RenderCameras": "", # 渲染相机，留空代表使用场景中设置的相机渲染
        "Renderable": True,
        "RenderWidth": "1920",
        "RenderHeight": "1080",
    }
})

param_check_obj.execute(**render_params)

# ========上传任务并提交==========
# 1. 获取 info.cfg 和 任务 ID 信息
info_path = analyze_obj.info_path
job_id = analyze_obj.job_id

# 2. 配置上传任务信息
upload_kwargs = {
    "api": api,
    "job_id": job_id,
    "info_path": info_path,
    "line": TransferLines.LINE_UNICOM,
    "speed": 200  # 上传速度限制，单位为 Mbps
}
# 3. 开始上传
renderg_upload = RenderGUpload(**upload_kwargs)
renderg_upload.upload()

# 4. 上传完成，提交任务，开始渲染
submit = api.job.submit_job(job_id)
logger.info(submit["msg"])

# 5. 下载
# 等待任务完成下载
download_kwargs = {
    "api": api,
    "job_id": job_id,
    "download_path": "d:/test",  # 下载保存到本地路径
    "line": TransferLines.LINE_UNICOM,
    "cluster_id": config["CLUSTER_ID"],
    "speed": 500  # 上传速度限制，单位为 Mbps
}
renderg_sync = RenderGDownload(**download_kwargs)
result = renderg_sync.auto_download_after_job_completed()

