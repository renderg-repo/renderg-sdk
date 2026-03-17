.. _analyze_maya:

analyze_maya
=============

``analyze_maya`` 包提供对 Maya 场景文件的自动分析功能，是 Maya 渲染提交流程的核心步骤。

主要包含两个类：

- :class:`~analyze_maya.analyze.AnalyzeMaya` —— 解析 Maya 场景文件，收集依赖资产（贴图、缓存、代理等），
  生成 ``info.cfg`` 资产清单，并向服务器创建渲染作业（Job）。
- :class:`~analyze_maya.param_check.ParamChecker` —— 在分析完成后，设置渲染参数（帧范围、渲染层、
  摄像机、分辨率等）并执行参数校验，最终将参数写入作业配置。

**典型使用流程**::

   from analyze_maya import AnalyzeMaya, ParamChecker

   analyze_obj = AnalyzeMaya(
       dcc_file=r"E:\Work\Scene\Maya\scene.ma",
       dcc_version="2025",
       project_path=r"E:\Work\Scene\Maya",
       api=api,
       project_id=42310,
       env_id=17877,
       workspace=workspace,
       logger=logger,
   )
   analyze_obj.analyze()

   param_check_obj = ParamChecker(api, analyze_obj)
   param_check_obj.set_render_layers({
       "defaultRenderLayer": {
           "ForceRenderFrames": "1-10",
           "RenderCameras": "",
           "Renderable": True,
           "RenderWidth": "1920",
           "RenderHeight": "1080",
       }
   })
   param_check_obj.execute(ChunkSize=1, zone_id=1009, ram_limit="64G")

完整示例请参考 :doc:`../example/submit_maya`。

.. toctree::
   :maxdepth: 4

   analyze_maya/analyze
   analyze_maya/param_check