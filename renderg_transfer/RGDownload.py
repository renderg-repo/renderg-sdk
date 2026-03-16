import json
import os
import time

from renderg_api.constants import JobStatus
import renderg_utils
from renderg_transfer.TransferHelper import TransferHelper
from renderg_transfer.MQClient import MqttClient


class RenderGDownload:
    """
    RenderG 文件下载类，用于从 RenderG 服务器下载渲染结果文件。

    支持两种下载方式：

    - **自动下载**：通过 MQTT 监听作业完成事件，作业渲染完成后自动触发下载（:meth:`auto_download_after_job_completed`）。
    - **自定义下载**：手动指定服务器路径进行下载（:meth:`custom_download`）。
    """

    def __init__(self, api, job_id, download_path, line, cluster_id, speed=1000, workspace=None, logger=None):
        """
        初始化文件下载实例。

        Args:
            api (RenderGAPI): RenderG API 实例。
            job_id (str or None): 作业 ID。若为 ``None``，则使用 ``cluster_id`` 获取传输配置
                                          （用于自定义下载场景）。
            download_path (str): 本地下载保存路径。
            line (int): 传输线路 ID，对应 :class:`~renderg_api.constants.TransferLines` 中的常量。
            cluster_id (str): 集群 ID，当 ``job_id`` 为 ``None`` 时使用。
            speed (int, optional): 传输速度限制（Mbps），默认为 1000。
            workspace (str, optional): 工作目录，用于存放日志文件。默认使用系统用户目录。
            logger (logging.Logger, optional): 日志记录器。默认使用全局 logger。
        """
        if logger is None:
            logger = renderg_utils.get_logger()
        self.logger = logger

        self.api = api
        if job_id is not None:
            self.transfer_config = api.transfer.get_transfer_config(job_id)
            self.user_id = self.transfer_config.get('username').split('_')[2]
        else:
            self.transfer_config = api.transfer.get_transfer_cluster(cluster_id)[0]
            self.user_id = self.transfer_config.get('username').split('_')[2]

        self.host, self.port = api.transfer.get_transfer_line(line)
        self.download_path = download_path
        self.job_id = job_id
        self.speed = speed

        self.workspace = renderg_utils.get_workspace(workspace)
        self.log_path = os.path.join(self.workspace, 'log')

        renderg_utils.check_path(self.workspace)
        renderg_utils.check_path(self.log_path)

        auth_key = self.api.mqConnect.get_key()
        self.mqtt_client = MqttClient('{}_{}_sdk'.format(self.user_id, time.time()), auth_key)
        self.jobEnd_list = []

    def mq_callback(self, result):
        """
        MQTT 消息回调函数，用于监听作业完成通知。

        当收到类型为 ``030003`` 的消息时，将对应的作业 ID 记录到完成列表中。

        Args:
            result (str): MQTT 消息内容（JSON 格式字符串）。
        """
        self.logger.info("Received message: " + result)
        payload = json.loads(result)
        if payload.get('type_id') == '030003':
            data = payload.get('data')
            job_id = data.get('job_id')
            self.jobEnd_list.append(str(job_id))

    def auto_download_after_job_completed(self):
        """
        等待作业渲染完成后自动下载结果文件。

        若作业尚未完成，该方法会通过 MQTT 订阅作业状态，阻塞等待直到收到渲染完成通知，
        然后使用 Aspera 协议下载渲染结果到 :attr:`download_path` 指定的本地目录。

        Raises:
            Exception: 当 Aspera 下载命令执行失败时抛出。
        """
        job_info = self.api.job.get_jobs_info(self.job_id)
        status = job_info.get('Status')
        if status != JobStatus.STATUS_COMPLETED:
            # 任务未完成，监听mqtt状态，等待完成
            self.logger.info("{} 任务未完成，等待渲染完成后下载···".format(self.job_id))
            self.mqtt_client.subscribe(
                'mqtt/front/user/{user_id}/{job_id}'.format(user_id=self.user_id, job_id=self.job_id),
                self.mq_callback
            )
            while True:
                if str(self.job_id) in self.jobEnd_list:
                    self.mqtt_client.unsubscribe(
                        'mqtt/front/user/{user_id}/{job_id}'.format(user_id=self.user_id, job_id=self.job_id)
                    )
                    break
                time.sleep(3)

        self.logger.info("{job_id}:渲染完成。开始下载".format(job_id=self.job_id))

        username = self.transfer_config.get("output_username")
        password = self.transfer_config.get("password")

        # 下载：
        cmd_pass = "set ASPERA_SCP_PASS={password}".format(password=password)
        files_source_path = './{job_id}/'.format(job_id=self.job_id)
        files_dest_path = self.download_path
        cmd = TransferHelper.create_ascp_command(
            cmd_pass=cmd_pass,
            mode="recv",
            host=self.host,
            port=self.port,
            username=username,
            max_speed=self.speed,
            log_dir=self.log_path,
            source_path=files_source_path,
            dest_path=files_dest_path
        )
        self.logger.info(cmd)
        code, stderr = renderg_utils.run_cmd(cmd, shell=True)
        self.logger.info("cmd return code: {}".format(code))
        if code != 0:
            raise Exception("{} 下载失败。error={}".format(self.job_id, stderr))

    def custom_download(self, server_path):
        """
        自定义下载，手动指定服务器路径下载文件到本地。

        Args:
            server_path (iterable): 服务器端待下载的路径集合，每个元素为一个服务器路径字符串。
                                    例如：``{"/{job_id}"}``。
                                    本地保存路径为 ``download_path/server_path``。

        Raises:
            Exception: 当 Aspera 下载命令执行失败时抛出。
        """
        username = self.transfer_config.get("output_username")
        password = self.transfer_config.get("password")

        source_paths = []
        dest_paths = []
        for source in server_path:
            source_paths.append(source)
            dest_paths.append("{}/{}".format(self.download_path, source))

        file_pair_list_path = TransferHelper.create_file_pair_list_file(
            self.workspace, source_paths, dest_paths
        )

        # 下载：
        cmd_pass = "set ASPERA_SCP_PASS={password}".format(password=password)

        cmd = TransferHelper.create_ascp_command(
            cmd_pass=cmd_pass,
            mode="recv",
            host=self.host,
            port=self.port,
            username=username,
            max_speed=self.speed,
            log_dir=self.log_path,
            pair_list_file=file_pair_list_path
        )
        self.logger.info(cmd)
        code, stderr = renderg_utils.run_cmd(cmd, shell=True)
        self.logger.info("cmd return code: {}".format(code))
        if code != 0:
            raise Exception("{} 下载失败。error={}".format(self.job_id, stderr))
