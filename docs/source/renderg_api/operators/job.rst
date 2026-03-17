renderg_api.operators.job
==============================

:class:`~renderg_api.operators.job.JobOperator` 提供渲染作业的完整生命周期管理，
通过 ``api.job`` 访问。

**典型工作流**::

   # 1. 创建作业（返回 job_id，通常由 AnalyzeMaya 等模块内部调用）
   job_id = api.job.new_job(dcc_file_path, project_id, env_id)

   # 2. 设置硬件配置
   api.job.set_job_config(job_id, zone=1009, ram="64G")

   # 3. 提交作业，开始渲染
   api.job.submit_job(job_id)

   # 4. 查询作业信息
   info = api.job.get_jobs_info(job_id)

   # 5. 控制作业
   api.job.stop_job([job_id])       # 暂停
   api.job.start_job([job_id])      # 恢复
   api.job.requeue_job([job_id])    # 重新排队
   api.job.speedup_job([job_id])    # 加速

.. automodule:: renderg_api.operators.job
   :members:
   :undoc-members:
   :show-inheritance:
