.. _analyze_clarisse_param_check:

analyze_clarisse.param_check
============================

该模块包含 ``ParamChecker`` 类，在 :class:`~analyze_clarisse.analyze.AnalyzeClarisse` 完成场景分析后，
负责设置渲染参数并将其写入服务器作业配置。

**主要步骤**：

1. 通过 ``set_render_layers(layers_dict)`` 指定要渲染的 Image 节点（渲染层）及帧范围
2. 调用 ``execute(**render_params)`` 进行参数校验并提交配置

**``set_render_layers`` 参数格式**::

   param_check_obj.set_render_layers({
       "project://render/cam2.color_sun_chr": "1-100",   # Image 节点路径: 帧范围
       "project://render/cam2.ID_chr":        "1-100",
   })

.. automodule:: analyze_clarisse.param_check
   :members:
   :undoc-members:
   :show-inheritance: