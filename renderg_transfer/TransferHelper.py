
import os
import json
import re
import time
import traceback

import renderg_utils


class TransferConstants:
    """
    文件传输配置文件 info.cfg 中的字段名常量。
    """

    ASSETS = 'Assets'       #: 资产列表字段名
    FULL_PATH = 'FullPath'  #: 本地完整路径字段名
    REMOTE_NAME = 'RemoteName'  #: 服务器端远程名称字段名
    FILE_TYPE = 'FileType'  #: 文件类型字段名，1 为配置文件，2 为资产文件
    MISSING = 'missing'     #: 文件缺失标志字段名，0 为存在，1 为缺失


class TransferHelper:
    """
    文件传输辅助工具类，提供 Aspera 传输命令构建、文件列表生成等静态方法。
    """

    @staticmethod
    def read_json(file_path):
        """
        读取 JSON 文件，自动尝试多种编码格式。

        Args:
            file_path (str): JSON 文件路径。

        Returns:
            dict: 解析后的 JSON 数据字典。若所有编码均解析失败则返回空字典 ``{}``。
        """
        encoding_list = ['utf-8-sig', 'utf-8', 'None', 'gb2312']
        for encoding in encoding_list:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    info_json = json.loads(f.read())
                return info_json
            except BaseException as e:
                traceback.print_exc()
        return {}

    @staticmethod
    def is_unc_path(path):
        """
        判断给定路径是否为 UNC 路径（IP 地址或域名开头的网络路径）。

        Args:
            path (str): 待检测的路径字符串。

        Returns:
            bool: 若为 UNC 路径则返回 ``True``，否则返回 ``False``。
        """
        upc_match = re.search(r'/?/?'
                              r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})'  # ip
                              r'|'
                              r'([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)'  # 域名
                              r'/.+', path)
        if upc_match:
            return True
        return False

    @staticmethod
    def handing_local_paths(paths):
        """

        Args:
            path: 本地文件路径

        Returns:
            规范路径后的本地文件路径
            :param paths:
        """
        if isinstance(paths, list):
            new_paths = []
            for path in paths:
                norma_path = os.path.normpath(path)
                norma_path.replace('\\', '/')
                new_paths.append(norma_path)
            return new_paths
        else:
            norma_path = os.path.normpath(paths)
            return norma_path.replace('\\', '/')

    @staticmethod
    def get_ascp_executable():
        """
        获取 Aspera ascp 可执行文件的绝对路径。

        Returns:
            str: ascp 可执行文件的绝对路径。
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, "../ascp/bin/ascp.exe"))
        return executable

    @classmethod
    def create_file_pair_list_file(cls, workspace, source_paths, dest_paths):
        """
        创建 Aspera ``--file-pair-list`` 所需的文件对列表文件。

        文件内容为源路径和目标路径交替排列的文本，每行一个路径。

        Args:
            workspace (str): 工作目录，文件将创建在 ``workspace/temp/`` 下。
            source_paths (list): 本地源文件路径列表。
            dest_paths (list): 服务器目标路径列表，与 ``source_paths`` 一一对应。

        Returns:
            str: 生成的文件对列表文件的绝对路径。
        """
        timestamp = time.time()
        formatted_time = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        file_path = os.path.join(
            workspace, "temp", 'transfer_files_{}.txt'.format(formatted_time)
        )
        renderg_utils.check_path(os.path.dirname(file_path))

        flist = [path for pair in zip(source_paths, dest_paths) for path in pair]
        with open(file_path, 'wb') as pf:
            pf.write('\n'.join(flist).encode('utf-8'))
            pf.write('\n'.encode('utf-8'))
        return file_path

    @classmethod
    def create_ascp_command(cls, cmd_pass, mode, host, port, username,
                            resume_check="2", max_speed=1000, log_dir="", pair_list_file="",
                            source_path=None, dest_path=None):
        """
        构建 Aspera ascp 传输命令字符串。

        Args:
            cmd_pass (str): 设置 ``ASPERA_SCP_PASS`` 环境变量的命令，例如
                            ``"set ASPERA_SCP_PASS=xxx"``。
            mode (str): 传输模式，``"send"`` 表示上传，``"recv"`` 表示下载。
            host (str): 传输服务器主机地址。
            port (int): 传输服务器端口。
            username (str): Aspera 用户名。
            resume_check (str, optional): 断点续传检查级别，默认为 ``"2"`` （校验文件大小和修改时间）。
            max_speed (int, optional): 最大传输速度（Mbps），默认为 1000。
            log_dir (str, optional): Aspera 日志目录。留空则不输出日志文件。
            pair_list_file (str, optional): ``--file-pair-list`` 文件路径。
                                             与 ``source_path``/``dest_path`` 二选一使用。
            source_path (str, optional): 单个源路径（下载时使用）。
            dest_path (str, optional): 单个目标路径（下载时使用）。

        Returns:
            str: 完整的 ascp 命令字符串，可直接传入 shell 执行。
        """
        ascp_executable = cls.get_ascp_executable()

        cmd = ('{cmd_pass}&& {ascp_dir} -P {port} -O {port} -T -l{speed}m --mode={mode} '
               '-k{resume_check} --policy=fair --overwrite=diff --user={username} -d --host={host} '
               '-Efiles.txt').format(
                username=username, cmd_pass=cmd_pass, ascp_dir=ascp_executable,
                host=host, port=port, speed=max_speed, mode=mode, resume_check=resume_check)
        if log_dir:
            cmd += " -L {log_path}".format(log_path=log_dir)

        if pair_list_file:
            cmd += " --file-pair-list={file_pair_list_path} .".format(file_pair_list_path=pair_list_file)

        if source_path:
            cmd += " {source_path}".format(source_path=source_path)

        if dest_path:
            cmd += " {dest_path}".format(dest_path=dest_path)

        return cmd
