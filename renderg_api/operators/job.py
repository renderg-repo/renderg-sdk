from renderg_api.connect import Connect
from renderg_api.constants import ControlType
from renderg_utils import *


class JobOperator(object):
    """
    渲染作业操作符类，用于管理渲染作业的创建、提交、控制和查询。
    """

    def __init__(self, connect: 'Connect'):
        """
        初始化作业操作符。
        
        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def new_job(self, dcc_file_path, project_id, env_id):
        """
        创建新的渲染作业。
        
        Args:
            dcc_file_path (str): DCC软件场景文件路径。
            project_id (str): 项目ID。
            env_id (str): 环境ID。
            
        Returns:
            str: 新创建的作业ID。
        """
        params = {
            'scene_path': dcc_file_path,
            'scene_type': SceneType.get_scene_file_type(dcc_file_path),
            'project_id': project_id,
            'env_id': env_id,
            'submit_type': 902,
            'transport': '2',

            # other msg
            'client_version': get_version(),
            'client_address': get_pc_ip(),
            'os': get_pc_version(),
            'mac': get_mac_address(),
            'submit_user': get_pc_name()
        }
        response = self._connect.post(self._connect.urls.NewJob, params)
        return response.get("job_id")

    def update_job_status(self, job_id, status, msg=""):
        """
        更新作业状态。
        
        Args:
            job_id (str): 作业ID。
            status (str): 新的状态。
            msg (str, optional): 状态更新消息。
            
        Returns:
            dict: 服务器响应。
        """
        params = {
            "job_id": job_id,
            "status": status,
            "msg": msg
        }
        return self._connect.post(self._connect.urls.UpdateJobStatus, params)

    def _control_job(self, job_ids: 'list', control_type, tiled_job_ids: 'list' = []):
        """
        控制作业的内部方法。
        
        Args:
            job_ids (list): 作业ID列表。
            control_type (str): 控制类型（开始、停止、加速、重新排队）。
            tiled_job_ids (list, optional): 分块作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        params = {
            'job_array': job_ids,
            'tiled_job_array': tiled_job_ids,
            "type": control_type
        }
        return self._connect.post(self._connect.urls.ControlJob, params)

    def start_job(self, job_ids: 'list', tiled_job_ids: 'list' = []):
        """
        开始作业。
        
        Args:
            job_ids (list): 作业ID列表。
            tiled_job_ids (list, optional): 分块作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        return self._control_job(job_ids, ControlType.START, tiled_job_ids)

    def stop_job(self, job_ids: 'list', tiled_job_ids: 'list' = []):
        """
        停止作业。
        
        Args:
            job_ids (list): 作业ID列表。
            tiled_job_ids (list, optional): 分块作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        return self._control_job(job_ids, ControlType.SUSPEND, tiled_job_ids)

    def speedup_job(self, job_ids: 'list', tiled_job_ids: 'list' = []):
        """
        加速作业。
        
        Args:
            job_ids (list): 作业ID列表。
            tiled_job_ids (list, optional): 分块作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        return self._control_job(job_ids, ControlType.SPEEDUP, tiled_job_ids)

    def requeue_job(self, job_ids: 'list', tiled_job_ids: 'list' = []):
        """
        重新排队作业。
        
        Args:
            job_ids (list): 作业ID列表。
            tiled_job_ids (list, optional): 分块作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        return self._control_job(job_ids, ControlType.REQUEUE, tiled_job_ids)

    def delete_job(self, job_ids: 'list'):
        """
        删除作业。
        
        Args:
            job_ids (list): 作业ID列表。
            
        Returns:
            dict: 服务器响应。
        """
        params = {'job_ids': job_ids}
        return self._connect.post(self._connect.urls.DelJob, params)

    def set_job_config(self, job_id, zone, ram):
        """
        设置作业配置。
        
        Args:
            job_id (str): 作业ID。
            zone (str): 区域ID。
            ram (int): RAM限制（MB）。
            
        Returns:
            dict: 服务器响应。
        """
        params = {
            'job_id': job_id,
            'ram_limit': ram,
            'cluster_id': self._connect.cluster_id,
            'zone_id': zone
        }
        return self._connect.post(self._connect.urls.SetJobConfig, params)

    def submit_job(self, job_id):
        """
        提交作业到渲染队列。
        
        Args:
            job_id (str): 作业ID。
            
        Returns:
            dict: 服务器响应。
        """
        params = {
            'job_id': job_id,
            'submit_version': "2"
        }
        return self._connect.post(self._connect.urls.SubmitJob, params)

    def get_jobs_info(self, job_id):
        """
        获取作业信息。
        
        Args:
            job_id (str): 作业ID。
            
        Returns:
            dict: 作业详细信息。
        """
        return self._connect.get(self._connect.urls.JobInfo + str(job_id))

    def get_job_list(self, page=1, count=20, json_params=None):
        """
        获取作业列表。

        参数:
            page (int): 页码，默认为1。
            count (int): 每页数量，默认为20。
            json_params (dict, optional): 过滤参数，可包含job_id_list、project_id、cluster_id等字段。

        返回:
            dict: 包含作业列表和分页信息的响应。
        """

        url_params = {
            'page': page,
            'count': count
        }

        return self._connect.post(self._connect.urls.GetJobList, data=json_params, params=url_params)
