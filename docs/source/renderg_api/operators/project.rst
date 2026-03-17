renderg_api.operators.project
===================================

:class:`~renderg_api.operators.project.ProjectOperator` 提供渲染项目的查询功能，
通过 ``api.project`` 访问。

项目（Project）是作业的归属容器，在 RenderG 客户端的项目管理界面创建后，
提交作业时需通过 ``project_id`` 指定所属项目。

**示例**::

   projects = api.project.get_project_list()
   for p in projects:
       print(p.get("id"), p.get("name"))

.. automodule:: renderg_api.operators.project
   :members:
   :undoc-members:
   :show-inheritance:
