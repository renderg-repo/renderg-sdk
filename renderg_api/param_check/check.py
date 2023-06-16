import os.path

import utils
from utils import RenderGException


class RenderGParamChecker(object):

    def __init__(self, api, analyze_obj):
        self.api = api
        self.analyze_obj = analyze_obj

        self.info_path = self.analyze_obj.info_path
        self.warning_path = self.analyze_obj.warning_path

    def execute(self, info_path=None, **kwargs):
        if info_path and os.path.isfile(info_path):
            self.info_path = info_path

        if "zone_id" not in kwargs:
            raise ValueError('Required "zone_id" not specified')
        if "ram_limit" not in kwargs:
            raise ValueError('Required "zone_id" not specified')

        self.api.set_hardware_config(self.analyze_obj.job_id, kwargs["zone_id"], kwargs["ram_limit"])

        self.set_custom_params(**kwargs)

    def set_custom_params(self, **kwargs):
        custom_params = {}
        info_data = utils.read_json(self.info_path)
        scene_type = utils.SceneType.get_scene_file_type(os.path.basename(self.analyze_obj.dcc_file))
        if scene_type == utils.SceneType.houdini:
            nodes = info_data.get("Nodes", {})
            custom_params = {
                    'ChunkSize': int(kwargs.get("ChunkSize", 1)),  # 一机多帧
                    'ForceRenderFrames': kwargs.get("ForceRenderFrames", ""),  # 帧范围
                    'Mark': kwargs.get("Mark", ""),  # 备注
                    'PriorityFrames':  kwargs.get("Mark", ""),  # 优先测试帧
                    'use_custom_params': 1,
                    'Nodes': self.__get_houdini_render_nodes(nodes),
                    'farm_envs': self.api.env.get_env_info_by_id(self.analyze_obj.env_id),
            }
        if not custom_params:
            raise ValueError('"CustomParams" is empty. please set it')

        info_data["CustomParams"] = custom_params
        utils.write_json(self.info_path, info_data)

    @staticmethod
    def __get_houdini_render_nodes(nodes):
        render_nodes = dict()
        for node_name, node_info in nodes.items():
            node_type = node_info.get("type")
            node_frame = node_info.get("Frames")
            if node_type == 'render_rop':
                render_nodes[node_name] = {
                    "Frames": node_frame
                }
        return render_nodes
