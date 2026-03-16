# RenderG SDK

RenderG SDK 是面向 [RenderG 云渲染平台](https://www.renderg.com/) 的 Python 客户端开发工具包，
帮助开发者将 DCC 软件的渲染工作流快速接入 RenderG 渲染农场。

## 功能特性

- **多 DCC 支持**：内置 Maya、Houdini、Clarisse 场景文件分析模块
- **自动资产收集**：分析场景依赖，生成资产清单（`info.cfg`），确保所有贴图、缓存、代理文件完整上传
- **高速文件传输**：基于 Aspera 协议的高速上传/下载，支持联通、电信多线路选择
- **完整作业管理**：创建、提交、暂停、恢复、加速、删除渲染作业及帧任务
- **实时状态监听**：通过 MQTT 订阅作业完成通知，渲染结束后自动下载结果

## 环境要求

- Python 2 / Python 3
- 依赖包：`requests`、`tenacity`、`paho-mqtt`、`typing_extensions`

## 安装

```shell
pip install renderg-sdk
```

或从源码安装：

```shell
git clone https://github.com/renderg-repo/renderg-sdk.git
cd renderg-sdk
pip install -e .
```

## 快速开始

### 1. 创建配置文件

在项目目录下新建 `config.json`：

```json
{
  "AUTH_KEY": "your_auth_key_here",
  "CLUSTER_ID": 27,
  "PROJECT_ID": 21479,
  "ENV_ID": 7715,
  "ZONE_ID": 1009,
  "RAM_LIMIT": "64G"
}
```

| 字段 | 说明 | 获取方式 |
|------|------|---------|
| `AUTH_KEY` | 用户身份认证密钥 | 联系 [RenderG 技术支持](https://www.renderg.com/) 获取 |
| `CLUSTER_ID` | 集群 ID | `api.config.get_cluster_list()` |
| `PROJECT_ID` | 项目 ID | `api.project.get_project_list()` |
| `ENV_ID` | 渲染环境 ID | `api.env.get_env_list()` |
| `ZONE_ID` | 硬件区域 ID | `api.config.get_zone_list()` |
| `RAM_LIMIT` | 内存限制 | `64G` / `128G` / `256G` |

### 2. 初始化 API

```python
from renderg_api import RenderGAPI
from renderg_utils import utils

config = utils.read_json("./config.json")
api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])
```

也可通过环境变量传入密钥，无需在代码中硬编码：

```shell
set RENDERG_AUTH_KEY=your_auth_key_here
```

```python
api = RenderGAPI(cluster_id=27)  # 自动读取环境变量 RENDERG_AUTH_KEY
```

---

## 提交示例

### Maya

```python
import os
from renderg_utils import utils, log
from analyze_maya import AnalyzeMaya, ParamChecker
from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.RGUpload import RenderGUpload
from renderg_transfer.RGDownload import RenderGDownload

config = utils.read_json("./config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()

api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

# 1. 分析场景，收集依赖资产
env_info = api.env.get_env_info_by_id(config["ENV_ID"])
analyze_obj = AnalyzeMaya(
    dcc_file=r"E:\Work\Scene\Maya\scene.ma",
    dcc_version="2025",
    project_path=env_info.get("project_path") or r"E:\Work\Scene\Maya",
    api=api,
    project_id=config["PROJECT_ID"],
    env_id=config["ENV_ID"],
    workspace=workspace,
    logger=logger,
)
analyze_obj.analyze()

# 2. 设置渲染参数
param_check_obj = ParamChecker(api, analyze_obj)
param_check_obj.set_render_layers({
    "defaultRenderLayer": {
        "ForceRenderFrames": "1-10",
        "RenderCameras": "",        # 留空使用场景默认相机
        "Renderable": True,
        "RenderWidth": "1920",
        "RenderHeight": "1080",
    }
})
param_check_obj.execute(
    ChunkSize=1,
    zone_id=config["ZONE_ID"],
    ram_limit=config["RAM_LIMIT"],
)

# 3. 上传资产
RenderGUpload(
    api=api,
    job_id=analyze_obj.job_id,
    info_path=analyze_obj.info_path,
    line=TransferLines.LINE_UNICOM,
    speed=200,
).upload()

# 4. 提交作业，开始渲染
api.job.submit_job(analyze_obj.job_id)

# 5. 等待完成后自动下载
RenderGDownload(
    api=api,
    job_id=analyze_obj.job_id,
    download_path="D:/renders/output",
    line=TransferLines.LINE_UNICOM,
    cluster_id=config["CLUSTER_ID"],
    speed=500,
).auto_download_after_job_completed()
```

### Houdini

```python
import os
from renderg_utils import utils, log
from analyze_houdini import AnalyzeHoudini, ParamChecker
from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.RGUpload import RenderGUpload
from renderg_transfer.RGDownload import RenderGDownload

config = utils.read_json("./config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()

api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

# 1. 分析场景，收集依赖资产
analyze_obj = AnalyzeHoudini(
    dcc_file=r"E:\Work\Scene\Houdini\scene.hip",
    dcc_version="20.5.584",
    api=api,
    project_id=config["PROJECT_ID"],
    env_id=config["ENV_ID"],
    workspace=workspace,
    logger=logger,
)
analyze_obj.analyze()

# 2. 设置渲染参数（指定 ROP 节点和帧范围）
param_check_obj = ParamChecker(api, analyze_obj)
param_check_obj.set_render_nodes({"/out/mantra1": "1-10"})
param_check_obj.execute(
    ChunkSize=1,
    zone_id=config["ZONE_ID"],
    ram_limit=config["RAM_LIMIT"],
)

# 3. 上传资产
RenderGUpload(
    api=api,
    job_id=analyze_obj.job_id,
    info_path=analyze_obj.info_path,
    line=TransferLines.LINE_UNICOM,
    speed=200,
).upload()

# 4. 提交作业，开始渲染
api.job.submit_job(analyze_obj.job_id)

# 5. 等待完成后自动下载
RenderGDownload(
    api=api,
    job_id=analyze_obj.job_id,
    download_path="D:/renders/output",
    line=TransferLines.LINE_UNICOM,
    cluster_id=config["CLUSTER_ID"],
    speed=500,
).auto_download_after_job_completed()
```

### Clarisse

```python
import os
from renderg_utils import utils, log
from analyze_clarisse import AnalyzeClarisse, ParamChecker
from renderg_api import RenderGAPI
from renderg_api.constants import TransferLines
from renderg_transfer.RGUpload import RenderGUpload
from renderg_transfer.RGDownload import RenderGDownload

config = utils.read_json("./config.json")
workspace = config.get("WORKSPACE", os.path.expandvars("%userprofile%/RenderG_WorkSpace"))

log.init_logging(log_dir=utils.get_workspace(workspace), console=True)
logger = log.get_logger()

api = RenderGAPI(auth_key=config["AUTH_KEY"], cluster_id=config["CLUSTER_ID"])

# 1. 分析场景，收集依赖资产
analyze_obj = AnalyzeClarisse(
    dcc_file=r"E:\Work\Scene\Clarisse\scene.project",
    dcc_version="5.0 SP11",
    api=api,
    project_id=config["PROJECT_ID"],
    env_id=config["ENV_ID"],
    workspace=workspace,
    logger=logger,
)
analyze_obj.analyze()

# 2. 设置渲染参数（指定 Image 节点路径和帧范围）
param_check_obj = ParamChecker(api, analyze_obj)
param_check_obj.set_render_layers({
    "project://render/cam2.color_sun_chr": "1-100",
    "project://render/cam2.ID_chr":        "1-100",
})
param_check_obj.execute(
    ChunkSize=1,
    zone_id=config["ZONE_ID"],
    ram_limit=config["RAM_LIMIT"],
)

# 3. 上传资产
RenderGUpload(
    api=api,
    job_id=analyze_obj.job_id,
    info_path=analyze_obj.info_path,
    line=TransferLines.LINE_UNICOM,
    speed=200,
).upload()

# 4. 提交作业，开始渲染
api.job.submit_job(analyze_obj.job_id)

# 5. 等待完成后自动下载
RenderGDownload(
    api=api,
    job_id=analyze_obj.job_id,
    download_path="D:/renders/output",
    line=TransferLines.LINE_UNICOM,
    cluster_id=config["CLUSTER_ID"],
    speed=500,
).auto_download_after_job_completed()
```

---

## 作业管理

```python
# 查询作业列表
jobs = api.job.get_job_list(page=1, count=20)

# 查询单个作业详情
info = api.job.get_jobs_info(job_id)

# 控制作业（支持列表批量操作）
api.job.stop_job([job_id])       # 暂停
api.job.start_job([job_id])      # 恢复
api.job.requeue_job([job_id])    # 重新排队
api.job.speedup_job([job_id])    # 加速
api.job.delete_job([job_id])     # 删除

# 查询并控制帧任务
tasks = api.task.get_task_list_by_job_id(job_id)
api.task.requeue_task(job_id, task_id_list=[234617690, 234617691])  # 重新渲染指定帧
```

## 错误处理

```python
from renderg_api.exception import RenderGAPIError

try:
    api.job.submit_job(job_id)
except RenderGAPIError as e:
    print("错误码:", e.err_code)
    print("错误信息:", e.err_msg)
    print("请求地址:", e.request_url)
```

## 完整示例

更多详细示例请参考 `example/` 目录：

- [`example/submit_maya.py`](example/submit_maya.py) — Maya 完整提交示例
- [`example/submit_houdini.py`](example/submit_houdini.py) — Houdini 完整提交示例
- [`example/submit_clarisse.py`](example/submit_clarisse.py) — Clarisse 完整提交示例
