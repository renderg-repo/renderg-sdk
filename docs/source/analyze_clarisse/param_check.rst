.. _analyze_clarisse_param_check:

analyze_clarisse.param_check
============================

该模块包含 ``ParamChecker`` 类，在 :class:`~analyze_clarisse.analyze.AnalyzeClarisse` 完成场景分析后，
负责设置渲染参数并将其写入服务器作业配置。

**主要步骤**：

1. 通过 ``set_render_layers(layers_dict)`` 指定要渲染的 Image 节点（渲染层）及帧范围
2. 调用 ``execute(**render_params)`` 进行参数校验并提交配置

.. warning::

   调用 ``execute()`` 前，``analyze_obj.job_id`` 必须已有效赋值。
   若在初始化分析对象时传入了 ``auto_create_job=False``，需先手动调用
   ``api.job.new_job()`` 并将返回值赋给 ``analyze_obj.job_id``，
   否则 ``execute()`` 将抛出 ``ValueError``。

**``set_render_layers`` 参数格式**::

   param_check_obj.set_render_layers({
       "project://render/cam2.color_sun_chr": "1-100",   # Image 节点路径: 帧范围
       "project://render/cam2.ID_chr":        "1-100",
   })

.. automodule:: analyze_clarisse.param_check
   :members:
   :undoc-members:
   :show-inheritance: