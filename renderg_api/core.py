import os

from renderg_api.connect import Connect
from renderg_api.operators import UserOperator, TaskOperator, JobOperator, ProjectOperator, EnvOperator, \
    TransferOperator, ConfigOperator
from renderg_api.mqConnect import MqConnect


class RenderGAPI(object):
    """
    RenderG SDK的核心API类，用于与RenderG渲染服务进行交互。
    
    该类提供了统一的接口，封装了与渲染服务的连接、用户管理、任务管理、作业管理等功能。
    """

    def __init__(self, auth_key=None, protocol='https', domain="client.renderg.com:6443", cluster_id=None):
        """
        初始化RenderGAPI实例。
        
        Args:
            auth_key (str, optional): 用户认证密钥。如果未提供，将尝试从环境变量RENDERG_AUTH_KEY获取。
            protocol (str, optional): 通信协议，默认为'https'。
            domain (str, optional): 服务器域名和端口，默认为'client.renderg.com:6443'。
            cluster_id (str, optional): 集群ID，用于指定使用的渲染集群。
            
        Raises:
            TypeError: 当未提供auth_key且环境变量中也不存在时抛出。
        """
        auth_key = auth_key or os.getenv("RENDERG_AUTH_KEY")
        if not auth_key:
            raise TypeError(
                'Required "auth_key" not specified. Pass as argument or set '
                'in environment variable RENDERG_AUTH_KEY.'
            )

        self._connect = Connect(auth_key, protocol, domain, cluster_id)

        self.user = UserOperator(self._connect)  # 用户操作符
        self.job = JobOperator(self._connect)  # 作业操作符
        self.task = TaskOperator(self._connect)  # 任务操作符
        self.project = ProjectOperator(self._connect)  # 项目操作符
        self.env = EnvOperator(self._connect)  # 环境操作符
        self.transfer = TransferOperator(self._connect)  # 传输操作符
        self.config = ConfigOperator(self._connect)  # 配置操作符
        self.mqConnect = MqConnect(auth_key)  # 消息队列连接

    def generate_job(self, dcc_file_path, project_name=None, env_name=None):
        """
        生成渲染作业。
        
        Args:
            dcc_file_path (str): DCC软件场景文件路径。
            project_name (str, optional): 项目名称。
            env_name (str, optional): 环境名称。
            
        Returns:
            作业ID或作业信息。
        """
        return self.job.new_job(dcc_file_path, project_name, env_name)

    def set_hardware_config(self, job_id, zone=None, ram=None):
        """
        设置作业的硬件配置。
        
        Args:
            job_id (str): 作业ID。
            zone (str, optional): 区域ID。
            ram (int, optional): RAM限制（MB）。
            
        Returns:
            设置结果。
        """
        return self.job.set_job_config(job_id, zone, ram)
