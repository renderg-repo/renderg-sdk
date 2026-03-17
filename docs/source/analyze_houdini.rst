.. _analyze_houdini:

analyze_houdini
===============

``analyze_houdini`` 包提供对 Houdini 场景文件（``.hip``）的自动分析功能，是 Houdini 渲染提交流程的核心步骤。

主要包含两个类：

- :class:`~analyze_houdini.analyze.AnalyzeHoudini` —— 解析 Houdini 场景文件，收集依赖资产，
  生成 ``info.cfg`` 资产清单，并向服务器创建渲染作业。
- :class:`~analyze_houdini.param_check.ParamChecker` —— 在分析完成后，设置渲染节点
  （ROP 节点，如 ``/out/mantra1``）及帧范围，并将参数写入作业配置。

**典型使用流程**::

   from analyze_houdini import AnalyzeHoudini, ParamChecker

   analyze_obj = AnalyzeHoudini(
       dcc_file=r"E:\Work\Scene\Houdini\scene.hip",
       dcc_version="20.5.584",
       api=api,
       project_id=42310,
       env_id=16884,
       workspace=workspace,
       logger=logger,
   )
   analyze_obj.analyze()

   param_check_obj = ParamChecker(api, analyze_obj)
   param_check_obj.set_render_nodes({"/out/mantra1": "1-10"})
   param_check_obj.execute(ChunkSize=1, zone_id=1009, ram_limit="64G")

**延后申请任务号** （``auto_create_job=False``）::

   # 分析阶段不申请任务号
   analyze_obj = AnalyzeHoudini(
       dcc_file=r"E:\Work\Scene\Houdini\scene.hip",
       dcc_version="20.5.584",
       api=api,
       project_id=42310,
       env_id=16884,
       auto_create_job=False,
   )
   analyze_obj.analyze()

   # 在此处加入业务判断（如人工审批、条件检查等）

   # 确认后手动申请，并绑定到分析对象
   analyze_obj.job_id = api.job.new_job(analyze_obj.dcc_file, 42310, 16884)

   # 后续与默认流程一致
   param_check_obj = ParamChecker(api, analyze_obj)
   param_check_obj.set_render_nodes({"/out/mantra1": "1-10"})
   param_check_obj.execute(zone_id=..., ram_limit=...)

完整示例请参考 :doc:`../example/submit_houdini`。

.. toctree::
   :maxdepth: 4

   analyze_houdini/analyze
   analyze_houdini/param_check