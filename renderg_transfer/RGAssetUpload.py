# coding=utf-8

import os
import time
import uuid

import renderg_utils
from renderg_transfer.AssetsPathHelper import AssetsPathHelper
from renderg_transfer.TransferHelper import TransferHelper
from renderg_utils.exception import AssetUploadError

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


class RenderGAssetUpload(object):
    """
    自定义资产上传类。

    将客户本地的文件或目录直接上传到 RenderG 存储，远端路径按本地目录结构自动生成，
    远端路径规则与作业资产上传一致：

    - D:/Project/tex      -> input/D/Project/tex
    - D:/Project/a.png    -> input/D/Project/a.png
    - //nas/share/tex     -> input/UNC/nas/share/tex

    Example::

        from renderg_transfer.RGAssetUpload import RenderGAssetUpload
        from renderg_api.constants import TransferLines

        uploader = RenderGAssetUpload(
            api=api,
            line=TransferLines.LINE_UNICOM,
            speed=1000,
        )
        uploader.upload([
            r"D:\Project\tex",
            r"D:\Project\models\hero.fbx",
        ])
    """

    def __init__(self, api, line, speed=1000, workspace=None, logger=None):
        """
        Args:
            api (RenderGAPI): 已初始化的 RenderG API 实例，需在构造时传入 cluster_id。
            line (int): 传输线路 ID，对应 renderg_api.constants.TransferLines。
            speed (int, optional): 最大传输速度（Mbps），默认为 1000。
            workspace (str, optional): 工作目录根路径，默认使用用户目录下的
                RenderG_WorkSpace。每次运行的日志目录会创建在该路径下。
            logger (logging.Logger, optional): 日志对象，未指定时使用全局 logger。
        """
        self.api = api
        self.line = line
        self.speed = 1000 if speed is None else speed
        self.cluster_id = getattr(api, "cluster_id", None)
        if not self.cluster_id:
            raise ValueError(
                'Required "cluster_id" not specified. '
                'Initialize RenderGAPI with cluster_id before uploading assets.'
            )

        if logger is None:
            logger = renderg_utils.get_logger()
        self.logger = logger
        self.workspace = renderg_utils.get_workspace(workspace)

    def upload(self, paths):
        """
        上传文件或目录到 RenderG 存储。

        Args:
            paths (str or list): 本地文件或目录路径，支持混合传入。路径会先转为绝对路径。

        Returns:
            list: [(local_path, remote_path), ...]，本次实际提交的文件/目录对。

        Raises:
            ValueError: 路径为空、不存在或参数类型不正确。
            AssetUploadError: ascp 返回码非 0。
        """
        run_dir, ascp_log_dir, manifest_path, manifest = self._init_run()

        try:
            entries = self._prepare_entries(paths)
            manifest["inputs"] = [
                {"source": entry["source"], "type": entry["type"], "dest": entry["dest"]}
                for entry in entries
            ]
            self._log_entries(entries)

            pair_file = self._write_pair_file(run_dir, entries)
            manifest.update({"pair_file": pair_file, "pair_count": len(entries)})
            self._write_manifest(manifest_path, manifest)

            username, password = self._get_transfer_account()
            host, port = self.api.transfer.get_transfer_line(self.line)
            manifest.update({"host": host, "port": port, "username": username})

            command, return_code, stderr_text, elapsed = self._run_ascp(
                pair_file, ascp_log_dir, username, password, host, port
            )
            manifest.update({
                "command": command,
                "return_code": return_code,
                "elapsed": round(elapsed, 3),
                "end_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ascp_log_files": self._list_files(ascp_log_dir),
            })

            if return_code != 0:
                manifest.update({"result": "failed", "stderr": stderr_text})
                self._write_manifest(manifest_path, manifest)
                self._error(
                    "upload failed. return_code=%s elapsed=%.3fs stderr=%s",
                    return_code, elapsed, stderr_text,
                )
                self._error("pair file kept for diagnosis: %s", pair_file)
                self._error("ascp log dir: %s", ascp_log_dir)
                self._error("run dir: %s", run_dir)
                raise AssetUploadError(
                    return_code, stderr_text, pair_file, ascp_log_dir, run_dir
                )

            manifest["result"] = "success"
            self._write_manifest(manifest_path, manifest)
            self._info(
                "upload success. pairs=%d elapsed=%.3fs run_dir=%s",
                len(entries), elapsed, run_dir,
            )
            self._remove_pair_file(pair_file)
            return [(entry["source"], entry["dest"]) for entry in entries]

        except AssetUploadError:
            raise
        except Exception as err:
            manifest["result"] = "failed"
            manifest["error"] = "{}: {}".format(type(err).__name__, err)
            manifest["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self._write_manifest(manifest_path, manifest)
            self._error("upload failed: %s: %s", type(err).__name__, err)
            self._error("run dir: %s", run_dir)
            raise

    def _init_run(self):
        self.run_id = "{}_{}".format(
            time.strftime("%Y%m%d_%H%M%S"), uuid.uuid4().hex[:6]
        )
        run_dir = os.path.join(self.workspace, "asset_upload", self.run_id)
        ascp_log_dir = os.path.join(run_dir, "ascp")
        renderg_utils.check_path(run_dir)
        renderg_utils.check_path(ascp_log_dir)

        proxy = getattr(self.api, "proxy", None) or {}
        manifest_path = os.path.join(run_dir, "manifest.json")
        manifest = {
            "run_id": self.run_id,
            "sdk_version": renderg_utils.get_version(),
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cluster_id": self.cluster_id,
            "line": self.line,
            "proxy": {
                "state": bool(proxy.get("state")),
                "host": proxy.get("host", ""),
                "api_port": proxy.get("api_port", ""),
                "scheme": proxy.get("scheme", "http"),
            },
            "speed_limit_mbps": self.speed,
            "workspace": self.workspace,
            "run_dir": run_dir,
            "inputs": [],
            "pair_file": None,
            "pair_count": 0,
            "ascp_log_dir": ascp_log_dir,
            "ascp_log_files": [],
            "command": "",
            "host": "",
            "port": "",
            "username": "",
            "return_code": None,
            "elapsed": None,
            "result": "running",
        }
        self._write_manifest(manifest_path, manifest)

        self._info(
            "start sdk=%s cluster_id=%s line=%s speed=%sMbps workspace=%s",
            manifest["sdk_version"], self.cluster_id, self.line, self.speed, self.workspace,
        )
        self._info("run_dir=%s", run_dir)
        if proxy.get("state"):
            self._info(
                "proxy enabled: host=%s api_port=%s scheme=%s",
                proxy.get("host"), proxy.get("api_port"), proxy.get("scheme", "http"),
            )
        return run_dir, ascp_log_dir, manifest_path, manifest

    def _log_entries(self, entries):
        file_count = len([entry for entry in entries if entry["type"] == "file"])
        self._info(
            "inputs: %d item(s), %d file(s), %d directories",
            len(entries), file_count, len(entries) - file_count,
        )
        for entry in entries:
            self._info(
                "%s %s -> %s",
                entry["type"].upper(), entry["source"], entry["dest"],
            )

    def _write_pair_file(self, run_dir, entries):
        pair_file = TransferHelper.create_file_pair_list_file(
            run_dir,
            [entry["source"] for entry in entries],
            [entry["dest"] for entry in entries],
        )
        self._info("pair file: %s (%d pairs)", pair_file, len(entries))
        return pair_file

    def _run_ascp(self, pair_file, ascp_log_dir, username, password, host, port):
        command = TransferHelper.create_ascp_command(
            cmd_pass=None,
            mode="send",
            host=host,
            port=port,
            username=username,
            max_speed=self.speed,
            log_dir=ascp_log_dir,
            pair_list_file=pair_file,
            exclude_files_txt=False,
        )
        self._info("ascp command: %s", command)
        self._info("ascp log dir: %s", ascp_log_dir)

        started = time.time()
        return_code, stderr = renderg_utils.run_cmd(
            command, shell=True, env={"ASPERA_SCP_PASS": password}
        )
        return command, return_code, self._to_text(stderr), time.time() - started

    def _prepare_entries(self, paths):
        """校验客户传入的文件/目录，并生成远端路径；不做目录遍历和额外过滤。"""
        if isinstance(paths, string_types):
            paths = [paths]
        if not isinstance(paths, (list, tuple)) or not paths:
            raise ValueError('"paths" must be a non-empty path or list of paths')

        entries = []
        for path in paths:
            if not isinstance(path, string_types):
                raise TypeError(
                    "path must be a string, got {}".format(type(path).__name__)
                )
            source = os.path.abspath(os.path.expanduser(os.path.normpath(path)))
            if not os.path.exists(source):
                raise ValueError("path does not exist: {}".format(source))
            entries.append({
                "source": source,
                "type": "directory" if os.path.isdir(source) else "file",
                "dest": AssetsPathHelper.assemble_server_input_path(source, source)[1],
            })
        return entries

    def _get_transfer_account(self):
        accounts = self.api.transfer.get_transfer_cluster(self.cluster_id)
        if isinstance(accounts, dict):
            accounts = [accounts]
        if not accounts:
            raise ValueError(
                "no transfer account found for cluster_id={}".format(self.cluster_id)
            )

        account = accounts[0]
        username = account.get("username")
        password = account.get("password")
        if not username or not password:
            raise ValueError(
                "transfer account missing username/password for cluster_id={}".format(
                    self.cluster_id
                )
            )
        return username, password

    @staticmethod
    def _to_text(value):
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", "ignore")
        return str(value)

    @staticmethod
    def _list_files(directory):
        try:
            return [
                os.path.join(directory, name)
                for name in os.listdir(directory)
            ]
        except Exception:
            return []

    @staticmethod
    def _remove_pair_file(pair_file):
        try:
            if pair_file and os.path.isfile(pair_file):
                os.remove(pair_file)
                parent = os.path.dirname(pair_file)
                if os.path.isdir(parent) and not os.listdir(parent):
                    os.rmdir(parent)
        except Exception:
            pass

    def _write_manifest(self, path, manifest):
        try:
            renderg_utils.write_json(path, manifest, ensure_ascii=True)
        except Exception as err:
            self.logger.warning(
                "[AssetUpload][%s] write manifest failed: %s", self.run_id, err
            )

    def _info(self, msg, *args):
        self.logger.info("[AssetUpload][%s] " + msg, self.run_id, *args)

    def _error(self, msg, *args):
        self.logger.error("[AssetUpload][%s] " + msg, self.run_id, *args)
