from renderg_api.connect import Connect
from renderg_api.constants import ControlType


class TaskOperator(object):
    """
    任务操作符类，用于管理渲染作业中各个帧任务的控制和查询。

    一个渲染作业（Job）由多个帧任务（Task）组成，每个任务对应一帧或一组帧的渲染。
    """

    def __init__(self, connect: 'Connect'):
        """
        初始化任务操作符。

        Args:
            connect (Connect): 与服务器的连接实例。
        """
        self._connect = connect

    def _control_task(self, job_id, control_type, task_id_list: 'list' = None):
        """Control tasks in a job.
        Args:
            job_id (int): The ID of the job containing the tasks.
            control_type (ControlType): The type of control operation to perform.
            task_id_list (list, optional): A list of task IDs to control.
                Example:
                    [234617690, 234617691]
        Returns:
            dict: The response from the control operation.
        """

        params = {
            'job_id': job_id,
            'task_array': task_id_list or [],
            "type": control_type
        }
        return self._connect.post(self._connect.urls.ControlTask, params)

    def start_task(self, job_id, task_id_list=None):
        """
        启动指定作业中的任务。

        Args:
            job_id (int): 作业 ID。
            task_id_list (list, optional): 要启动的任务 ID 列表。
                                            若为 ``None`` 或空列表，则启动该作业下的所有任务。

        Returns:
            dict: 服务器响应。
        """
        return self._control_task(job_id=job_id, control_type=ControlType.START, task_id_list=task_id_list or [])

    def stop_task(self, job_id, task_id_list=None):
        """
        暂停指定作业中的任务。

        Args:
            job_id (int): 作业 ID。
            task_id_list (list, optional): 要暂停的任务 ID 列表。
                                            若为 ``None`` 或空列表，则暂停该作业下的所有任务。

        Returns:
            dict: 服务器响应。
        """
        return self._control_task(job_id=job_id, control_type=ControlType.SUSPEND, task_id_list=task_id_list or [])

    def requeue_task(self, job_id, task_id_list=None):
        """
        将指定作业中的任务重新加入渲染队列。

        常用于任务失败后重新渲染。

        Args:
            job_id (int): 作业 ID。
            task_id_list (list, optional): 要重新排队的任务 ID 列表。
                                            若为 ``None`` 或空列表，则对该作业下的所有任务重新排队。

        Returns:
            dict: 服务器响应。
        """
        return self._control_task(job_id=job_id, control_type=ControlType.REQUEUE, task_id_list=task_id_list or [])

    def __get_task_list(self, page=0, count=20, json_params=None):
        """
        Retrieve a paginated list of tasks.

        Args:
            page (int): The page number to retrieve. Defaults to 1.
            count (int): The number of tasks per page. Defaults to 20.
            json_params (dict, optional): Additional filtering parameters for the task list.
                Example:
                    {
                        "desc": true,
                        "job_farm_id": "",
                        "sort": "",
                        "stat": "",
                        "frame": null,
                        "job_id": 6666666
                    }

        Returns:
            dict: The response containing the task list and pagination details.
        """
        url_params = {
            'page': page,
            'count': count
        }
        if json_params is None:
            json_params = {}
        if not isinstance(json_params, dict):
            raise TypeError('json_params must be a dict, got {}'.format(type(json_params)))

        return self._connect.post(self._connect.urls.GetTaskList, data=json_params, params=url_params)

    def get_task_list_by_job_id(self, job_id, page=0, count=20):
        """
        根据作业 ID 获取该作业下的任务列表（分页）。

        Args:
            job_id (int): 作业 ID。
            page (int, optional): 页码，从 0 开始，默认为 0。
            count (int, optional): 每页返回的任务数量，默认为 20。

        Returns:
            dict: 包含任务列表和分页信息的响应字典。
        """
        json_params = {
            'job_id': job_id
        }
        return self.__get_task_list(page=page, count=count, json_params=json_params)
