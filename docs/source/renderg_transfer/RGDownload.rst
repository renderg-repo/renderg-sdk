renderg_transfer.RGDownload
==============================

:class:`~renderg_transfer.RGDownload.RenderGDownload` 封装了从 RenderG 服务器下载渲染结果的逻辑，
支持两种模式：

- **自动下载**：通过 MQTT 监听作业完成通知，渲染完成后自动触发下载。
- **自定义下载**：手动指定服务器路径，适用于下载历史作业或部分结果。

**自动下载示例**::

   from renderg_transfer.RGDownload import RenderGDownload
   from renderg_api.constants import TransferLines

   download = RenderGDownload(
       api=api,
       job_id=job_id,
       download_path="D:/renders/output",
       line=TransferLines.LINE_UNICOM,
       cluster_id=config["CLUSTER_ID"],
       speed=500,
   )
   download.auto_download_after_job_completed()  # 阻塞等待渲染完成后下载

**自定义下载示例**::

   download = RenderGDownload(
       api=api,
       job_id=None,
       download_path="D:/renders/output",
       line=TransferLines.LINE_UNICOM,
       cluster_id=config["CLUSTER_ID"],
   )
   download.custom_download(server_path={"/{job_id}".format(job_id=123456)})

.. automodule:: renderg_transfer.RGDownload
   :members:
   :undoc-members:
   :show-inheritance:
