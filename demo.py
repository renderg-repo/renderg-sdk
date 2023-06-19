import os

import utils
from analyze_houdini import AnalyzeHoudini
from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_api.param_check import RenderGParamChecker
from renderg_upload.rgUpload import RendergUpload

config = utils.read_json("./config.json")

api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

# analyze DCC file
analyze_info = {
    "dcc_file": r"D:\houdini_file\JSBL_lgt_qunji_wmy_v001.hip",
    "dcc_version": "19.0.622",
    "workspace": r"D:\workspace",  # 工作目录，存放日志、分析结果等文件。默认为 %USERPROFILE%\RenderG_WorkSpace
    "api": api,
    "project_id": config["PROJECT_ID"],  # 项目ID
    "env_id": config["ENV_ID"],  # 环境ID
    "job_id": None,  # 任务号为空时，自动创建任务号
}

analyze_obj = AnalyzeHoudini(**analyze_info)
analyze_obj.analyze()
print(analyze_obj.info_path)


param_check_obj = RenderGParamChecker(api, analyze_obj)
render_params = {
    "ChunkSize": 1,  # 一机多帧
    "Mark": "",  # 任务备注信息
    "PriorityFrames": "010:",  # 优先渲染帧 例：101:100-108x2 代表渲染首尾帧和100-108步长为2的帧

    "zone_id": config["ZONE_ID"],  # 渲染节点配置ID
    "ram_limit": config["RAM_LIMIT"],  # 渲染节点内存配置
}
param_check_obj.execute(**render_params)

# upload assets
info_path = analyze_obj.info_path
job_id = analyze_obj.job_id

kwargs = {
    "api": api,
    "job_id": job_id,
    "info_path": info_path,
    "line": TransferLines.LINE_RENDERG,
    "spend": 200
}
renderg_upload = RendergUpload(**kwargs)
renderg_upload.upload()

# submit job
submit = api.job.submit_job(job_id)
print(submit["msg"])
