.. _analyze_clarisse:

analyze_clarisse
================

``analyze_clarisse`` 包提供对 Clarisse iFX 场景文件（``.project``）的自动分析功能，是 Clarisse 渲染提交流程的核心步骤。

主要包含两个类：

- :class:`~analyze_clarisse.analyze.AnalyzeClarisse` —— 解析 Clarisse 场景文件，收集依赖资产，
  生成 ``info.cfg`` 资产清单，并向服务器创建渲染作业。
- :class:`~analyze_clarisse.param_check.ParamChecker` —— 在分析完成后，设置渲染层
  （Image 节点路径，如 ``project://render/cam2.color_sun_chr``）及帧范围，
  并将参数写入作业配置。

**典型使用流程**::

   from analyze_clarisse import AnalyzeClarisse, ParamChecker

   analyze_obj = AnalyzeClarisse(
       dcc_file=r"E:\Work\Scene\Clarisse\scene.project",
       dcc_version="5.0 SP11",
       api=api,
       project_id=42310,
       env_id=5335,
       workspace=workspace,
       logger=logger,
   )
   analyze_obj.analyze()

   param_check_obj = ParamChecker(api, analyze_obj)
   param_check_obj.set_render_layers({
       "project://render/cam2.color_sun_chr": "1-100",
   })
   param_check_obj.execute(ChunkSize=1, zone_id=1009, ram_limit="64G")

**延后申请任务号** （``auto_create_job=False``）::

   # 分析阶段不申请任务号
   analyze_obj = AnalyzeClarisse(
       dcc_file=r"E:\Work\Scene\Clarisse\scene.project",
       dcc_version="5.0 SP11",
       api=api,
       project_id=42310,
       env_id=5335,
       auto_create_job=False,
   )
   analyze_obj.analyze()

   # 在此处加入业务判断（如人工审批、条件检查等）

   # 确认后手动申请，并绑定到分析对象
   analyze_obj.job_id = api.job.new_job(analyze_obj.dcc_file, 42310, 5335)

   # 后续与默认流程一致
   param_check_obj = ParamChecker(api, analyze_obj)
   param_check_obj.set_render_layers({...})
   param_check_obj.execute(zone_id=..., ram_limit=...)

完整示例请参考 :doc:`../example/submit_clarisse`。

.. toctree::
   :maxdepth: 4

   analyze_clarisse/analyze
   analyze_clarisse/param_check