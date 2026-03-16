
import os

from renderg_api.constants import JobStatus
from renderg_transfer.AssetsPathHelper import AssetsPathHelper
from renderg_transfer.TransferHelper import TransferHelper

import renderg_utils


class RenderGUpload:
    """
    RenderG文件上传类，用于将渲染资产上传到RenderG服务器。
    
    该类封装了使用Aspera协议进行高效文件传输的功能，包括资产路径处理、传输配置管理和上传过程监控。
    """

    def __init__(self, api, job_id, info_path, line, speed, workspace=None, logger=None):
        """
        初始化文件上传实例。
        
        Args:
            api (RenderGAPI): RenderG API实例。
            job_id (str): 作业ID。
            info_path (str): 资产信息配置文件路径。
            line (str): 传输线路。
            speed (int, optional): 传输速度限制（KB/s）。
            workspace (str, optional): 工作目录。
            logger (logging.Logger, optional): 日志记录器。
        """
        if logger is None:
            logger = renderg_utils.get_logger()
        self.logger = logger

        self.api = api
        self.transfer_config = api.transfer.get_transfer_config(job_id)
        self.transfer_lines = api.transfer.get_transfer_line(line)
        self.info_path = info_path
        self.job_id = job_id
        if speed is not None:
            self.speed = speed
        else:
            self.speed = 1000
        self.workspace = os.path.join(renderg_utils.get_workspace(workspace), str(self.job_id))
        self.log_path = os.path.join(renderg_utils.get_workspace(workspace), 'log')
        renderg_utils.check_path(self.workspace)
        renderg_utils.check_path(self.log_path)

    def upload(self):
        """
        执行文件上传操作。
        
        该方法会：
        1. 更新作业状态为上传中
        2. 从配置文件中获取源文件路径和目标路径
        3. 构建Aspera传输命令
        4. 执行上传命令
        5. 处理上传结果
        
        Raises:
            Exception: 当上传失败时抛出异常。
        """
        self.api.job.update_job_status(self.job_id, JobStatus.STATUS_UPLOAD)
        source_paths, dest_paths = AssetsPathHelper.get_file_list_for_info_cfg(self.info_path, self.job_id)

        host, port = self.transfer_lines
        username = self.transfer_config.get("username")
        password = self.transfer_config.get("password")

        file_pair_list_path = TransferHelper.create_file_pair_list_file(
            self.workspace, source_paths, dest_paths
        )

        cmd_pass = "set ASPERA_SCP_PASS={password}".format(password=password)
        cmd = TransferHelper.create_ascp_command(
            cmd_pass=cmd_pass,
            mode="send",
            host=host,
            port=port,
            username=username,
            max_speed=self.speed,
            log_dir=self.log_path,
            pair_list_file=file_pair_list_path
        )
        self.logger.info(cmd)
        code, stderr = renderg_utils.run_cmd(cmd, shell=True)
        self.logger.info("cmd return code: {}".format(code))
        if code != 0:
            raise Exception("{} 上传失败。 error={}".format(self.job_id, stderr.read()))
