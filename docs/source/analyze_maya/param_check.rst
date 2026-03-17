.. _analyze_maya_param_check:

analyze_maya.param_check
========================

该模块包含 ``ParamChecker`` 类，在 :class:`~analyze_maya.analyze.AnalyzeMaya` 完成场景分析后，
负责设置渲染参数并将其写入服务器作业配置。

**主要步骤**：

1. 通过 ``set_render_layers(layers_dict)`` 设置要渲染的层及每层的帧范围、摄像机、分辨率等参数
2. 调用 ``execute(**render_params)`` 进行参数校验并提交配置

**``set_render_layers`` 参数格式**::

   param_check_obj.set_render_layers({
       "defaultRenderLayer": {
           "ForceRenderFrames": "1-100",   # 强制渲染帧范围
           "RenderCameras": "cam1",        # 渲染相机，留空使用场景默认
           "Renderable": True,             # 是否渲染该层
           "RenderWidth": "1920",
           "RenderHeight": "1080",
       }
   })

.. automodule:: analyze_maya.param_check
   :members:
   :undoc-members:
   :show-inheritance: