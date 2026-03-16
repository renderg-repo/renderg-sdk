import os
from renderg_transfer.TransferHelper import TransferConstants, TransferHelper


class AssetsPathHelper:
    """
    资产路径辅助工具类，用于解析 info.cfg 配置文件并生成上传所需的源路径和目标路径列表。
    """

    @staticmethod
    def get_file_list_for_info_cfg(info_path, job_id):
        """
        解析资产信息配置文件（info.cfg），生成上传用的本地源路径和服务器目标路径列表。

        Args:
            info_path (str): info.cfg 配置文件的本地路径。
            job_id (str): 作业 ID，用于构建服务器端目标路径。

        Returns:
            tuple: ``(source_paths, dest_paths)``，分别为本地源路径列表和服务器目标路径列表。
                   若 info.cfg 文件不存在或解析失败，则两个列表均为空。
        """
        source_paths = []
        dest_paths = []

        if os.path.isfile(info_path):
            info_json = TransferHelper.read_json(info_path)
            if info_json:
                source_paths, dest_paths = AssetsPathHelper.__get_file_list_for_info_cfg(
                    job_id, info_json, TransferConstants.ASSETS, info_path)

        return source_paths, dest_paths

    @staticmethod
    def __get_file_list_for_info_cfg(job_id, info_json, key, info_path=None):
        source_paths = []
        dest_paths = []

        assets_list = info_json.get(key)
        for path_dict in assets_list:
            full_path = TransferHelper.handing_local_paths(
                path_dict.get(TransferConstants.FULL_PATH)
            )
            remote_name = TransferHelper.handing_local_paths(
                path_dict.get(TransferConstants.REMOTE_NAME)
            )
            file_type = int(path_dict.get(TransferConstants.FILE_TYPE))
            missing = int(path_dict.get(TransferConstants.MISSING))
            if missing == 0:
                if file_type == 1:
                    source_paths.append(full_path)
                    dest_paths.append(
                        AssetsPathHelper.assemble_server_cfg_path(job_id, full_path)
                    )
                elif file_type == 2:
                    local_paths, server_paths = \
                        AssetsPathHelper.assemble_server_input_path(full_path, remote_name)
                    source_paths.append(local_paths)
                    dest_paths.append(server_paths)

        if os.path.isfile(info_path):
            source_paths.insert(0, info_path)
            dest_paths.insert(0, AssetsPathHelper.assemble_server_cfg_path(job_id, info_path))

        return source_paths, dest_paths

    @staticmethod
    def assemble_server_cfg_path(job_id, path):
        """
        根据作业 ID 和本地文件路径，构建服务器端配置文件存储路径。

        Args:
            job_id (str): 作业 ID。
            path (str): 本地文件路径，取文件名部分。

        Returns:
            str: 服务器端路径，格式为 ``cfg/{job_id}/{filename}``。
        """
        filename = os.path.basename(path)
        cfg_path = 'cfg/{job_id}/{filename}'.format(job_id=job_id, filename=filename)
        return cfg_path.replace('\\', '/')

    @staticmethod
    def assemble_server_input_path(local_path, remote_name):
        """
        将本地文件路径转换为服务器端的 input 存储路径。

        支持 Windows 盘符路径（如 ``E:/Work/file.ext``）、UNC 网络路径、
        以及 Linux 风格路径的转换。

        Args:
            local_path (str): 本地文件绝对路径。
            remote_name (str): 资产的远程名称（通常为 info.cfg 中 ``RemoteName`` 字段的值）。

        Returns:
            tuple: ``(normalized_local_path, server_path)``，
                   分别为规范化后的本地路径（使用正斜杠）和服务器端目标路径。
        """
        norma_path = TransferHelper.handing_local_paths(os.path.normpath(local_path))
        norma_name = TransferHelper.handing_local_paths(os.path.normpath(remote_name))

        split_path = norma_name.split(':')
        if len(split_path) == 2:
            driver = split_path[0].upper().strip('/')
            file = split_path[1].strip('/')
            server_path = 'input/{driver}/{file}'.format(driver=driver, file=file)
        else:
            split_path = norma_name.split('/')
            if len(split_path) >= 2:
                driver_name = split_path[0].split('_')
                if len(driver_name) == 2:
                    driver = driver_name[1].upper().strip('/')
                    file = '/'.join(split_path[1:])
                    file = file.strip('/')
                    server_path = 'input/{driver}/{file}'.format(driver=driver, file=file)
                else:
                    if TransferHelper.is_unc_path(norma_name):
                        server_path = 'input/UNC/{}'.format(norma_name.strip("/"))
                    else:
                        server_path = 'input/{}'.format(norma_name.strip("/"))
            else:
                server_path = os.path.join('input/{}'.format(norma_name.strip("/")))

        return norma_path.replace('\\', '/'), server_path.replace('\\', '/')
