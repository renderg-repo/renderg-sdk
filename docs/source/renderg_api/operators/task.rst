renderg_api.operators.task
===============================

:class:`~renderg_api.operators.task.TaskOperator` 提供对作业内帧任务（Task）的控制和查询，
通过 ``api.task`` 访问。一个作业由多个帧任务组成，每个任务对应一帧或一组帧的渲染。

**示例**::

   # 查询作业下的任务列表（第 1 页，每页 20 条）
   tasks = api.task.get_task_list_by_job_id(job_id=123456)

   # 对失败的帧重新排队（不传 task_id_list 则对所有任务操作）
   api.task.requeue_task(job_id=123456, task_id_list=[234617690, 234617691])

   # 暂停 / 恢复全部任务
   api.task.stop_task(job_id=123456)
   api.task.start_task(job_id=123456)

.. automodule:: renderg_api.operators.task
   :members:
   :undoc-members:
   :show-inheritance:
