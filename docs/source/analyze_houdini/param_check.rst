.. _analyze_houdini_param_check:

analyze_houdini.param_check
===========================

该模块包含 ``ParamChecker`` 类，在 :class:`~analyze_houdini.analyze.AnalyzeHoudini` 完成场景分析后，
负责设置渲染参数并将其写入服务器作业配置。

**主要步骤**：

1. 通过 ``set_render_nodes(nodes_dict)`` 指定要渲染的 ROP 节点及帧范围
2. 调用 ``execute(**render_params)`` 进行参数校验并提交配置

**``set_render_nodes`` 参数格式**::

   param_check_obj.set_render_nodes({
       "/out/mantra1": "1-100",    # ROP 节点路径: 帧范围
       "/out/karma1":  "1-100",
   })

.. automodule:: analyze_houdini.param_check
   :members:
   :undoc-members:
   :show-inheritance: