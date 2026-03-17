renderg_api.operators.config
==================================

:class:`~renderg_api.operators.config.ConfigOperator` 提供集群和区域（Zone）硬件配置的查询功能，
通过 ``api.config`` 访问。

- **集群（Cluster）**：渲染节点的物理集群，``CLUSTER_ID`` 通常在初始化 :class:`~renderg_api.core.RenderGAPI` 时指定。
- **区域（Zone）**：集群内的硬件规格分组，提交作业时通过 ``zone_id`` 指定 CPU 型号、核心数等。

**示例**::

   # 查看所有集群
   clusters = api.config.get_cluster_list()

   # 查看指定集群下的区域配置
   zones = api.config.get_zone_list(cluster_id="27")
   for zone in zones.get("data", []):
       print(zone.get("id"), zone.get("name"))

.. automodule:: renderg_api.operators.config
   :members:
   :undoc-members:
   :show-inheritance:
