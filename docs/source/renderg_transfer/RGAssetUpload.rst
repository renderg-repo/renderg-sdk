renderg_transfer.RGAssetUpload
===============================

:class:`~renderg_transfer.RGAssetUpload.RenderGAssetUpload` 将客户本地的文件或目录直接上传到
RenderG 存储，不创建渲染作业。文件和目录都作为一对 source/dest 写入同一个
``--file-pair-list``，由一次 ascp 调用完成；目录不做遍历。

远端路径按本地目录结构自动生成：

- ``D:/Project/tex`` -> ``input/D/Project/tex``
- ``D:/Project/a.png`` -> ``input/D/Project/a.png``
- ``//nas/share/tex`` -> ``input/UNC/nas/share/tex``

如果客户使用 RenderG 定制代理程序，初始化 ``RenderGAPI`` 时传入 ``proxy`` 配置，
SDK 会通过代理的 ``/config`` 自动映射 ascp 的 host/port::

   api = RenderGAPI(
       auth_key=config["AUTH_KEY"],
       cluster_id=config["CLUSTER_ID"],
       proxy=config.get("PROXY"),
   )

**使用示例**::

   from renderg_api import RenderGAPI
   from renderg_api.constants import TransferLines
   from renderg_transfer.RGAssetUpload import RenderGAssetUpload

   api = RenderGAPI(
       auth_key=config["AUTH_KEY"],
       cluster_id=config["CLUSTER_ID"],
       proxy=config.get("PROXY"),
   )
   uploader = RenderGAssetUpload(
       api=api,
       line=TransferLines.LINE_UNICOM,
       speed=1000,
   )
   uploader.upload([
       "D:/Project/tex",
       "D:/Project/models/hero.fbx",
   ])

失败以 ascp 返回码判断，非 0 抛出 :class:`~renderg_utils.exception.AssetUploadError`。
每次运行的 ``manifest.json``、pair 文件和 ascp 日志保存在
``{workspace}/asset_upload/{run_id}/``。

.. automodule:: renderg_transfer.RGAssetUpload
   :members:
   :undoc-members:
   :show-inheritance:
