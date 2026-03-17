renderg_api.operators.user
=================================

:class:`~renderg_api.operators.user.UserOperator` 提供用户账户相关的查询功能，
通过 ``api.user`` 访问。

**示例**::

   # 获取可用集群列表
   clusters = api.user.get_cluster_list()
   for c in clusters:
       print(c)   # 包含集群 ID、名称等

   # 获取可用区域（Zone）配置
   zones = api.user.get_zone_list()

.. note::

   查询集群/区域列表也可通过 ``api.config`` 访问，:class:`~renderg_api.operators.config.ConfigOperator`
   提供了更丰富的过滤参数。

.. automodule:: renderg_api.operators.user
   :members:
   :undoc-members:
   :show-inheritance:
