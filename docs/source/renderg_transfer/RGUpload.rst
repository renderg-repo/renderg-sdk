renderg_transfer.RGUpload
==============================

:class:`~renderg_transfer.RGUpload.RenderGUpload` 封装了使用 Aspera 高速协议将场景文件和资产
上传到 RenderG 服务器的全部逻辑。

上传前需先通过 DCC 分析模块（如 :class:`~analyze_maya.analyze.AnalyzeMaya`）生成 ``info.cfg``
资产清单文件，上传器据此文件确定待传文件列表。

**使用示例**::

   from renderg_transfer.RGUpload import RenderGUpload
   from renderg_api.constants import TransferLines

   upload = RenderGUpload(
       api=api,
       job_id=job_id,
       info_path=analyze_obj.info_path,
       line=TransferLines.LINE_UNICOM,
       speed=200,          # 速度限制，单位 Mbps
   )
   upload.upload()

.. automodule:: renderg_transfer.RGUpload
   :members:
   :undoc-members:
   :show-inheritance:
