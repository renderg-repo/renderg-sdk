import logging
import os
import re
import uuid

from renderg_api.constants import JobStatus
from renderg_utils import RenderGException

try:
    import _winreg
    winreg = _winreg
except ImportError:
    import winreg

from renderg_utils.exception import DCCFileNotExistsError
from renderg_utils.exception import DCCExeNotFoundError
from renderg_utils.exception import AnalyzeFailError
from renderg_utils.exception import ErrorCode, WarnCode

import renderg_utils


class AnalyzeMaya(object):
    def __init__(self,
                 dcc_file,
                 dcc_version,
                 project_path,
                 workspace=None,
                 dcc_exe_path=None,
                 api=None,
                 project_id=None,
                 env_id=None,
                 job_id=None,
                 auto_create_job=True,
                 logger=None
                 ):

        """
        Args:
            dcc_file (str): Maya 场景文件的绝对路径（``.ma`` 或 ``.mb``）。
            dcc_version (str): Maya 版本号，例如 ``"2025"``。
            project_path (str): Maya 项目根目录路径。
            workspace (str, optional): 本地工作目录根路径，用于存放分析产物。
                默认使用系统用户目录下的 ``RenderG_WorkSpace``。
            dcc_exe_path (str, optional): ``mayabatch.exe`` 的完整路径。
                未指定时自动从注册表查找。
            api (RenderGAPI, optional): 已实例化的 API 对象。
            project_id (int, optional): RenderG 项目 ID。
            env_id (int, optional): RenderG 渲染环境 ID。
            job_id (str, optional): 已有的任务号。传入后直接使用，不再申请新任务号。
            auto_create_job (bool, optional): 是否在初始化时自动申请任务号，默认为 ``True``。
                设为 ``False`` 时，初始化阶段不向服务端申请任务号，本地工作目录以 UUID 命名；
                需在调用 ``param_check.execute()`` 前手动调用 ``api.job.new_job()``
                并将返回值赋给 ``analyze_obj.job_id``。
            logger (logging.Logger, optional): 日志对象，未指定时使用根 Logger。

        Example:
            默认行为，初始化时自动申请任务号::

                analyze_obj = AnalyzeMaya(
                    dcc_file=r"E:\\scene.ma",
                    dcc_version="2025",
                    project_path=r"E:\\scene",
                    api=api, project_id=42310, env_id=17877,
                )

            延后申请任务号（``auto_create_job=False``）::

                analyze_obj = AnalyzeMaya(
                    dcc_file=r"E:\\scene.ma",
                    dcc_version="2025",
                    project_path=r"E:\\scene",
                    api=api, project_id=42310, env_id=17877,
                    auto_create_job=False,
                )
                analyze_obj.analyze()
                analyze_obj.job_id = api.job.new_job(analyze_obj.dcc_file, 42310, 17877)
        """
        if not os.path.isfile(dcc_file):
            raise DCCFileNotExistsError(ErrorCode.DCCFileNotExistsError, dcc_file)

        self.dcc_file = dcc_file
        self.dcc_version = dcc_version
        self.project_path = project_path
        if not self.project_path or not os.path.isdir(self.project_path):
            raise RenderGException(ErrorCode.MayaProjectInvalidError, self.project_path)

        self.dcc_exe_path = dcc_exe_path
        self.api = api
        self.project_id = project_id
        self.env_id = env_id
        self.job_id = job_id

        if logger is None:
            logger = logging.getLogger()
        self.logger = logger

        if not job_id:
            if auto_create_job:
                self.job_id = self.api.job.new_job(self.dcc_file, self.project_id, self.env_id)

        _local_id = str(self.job_id) if self.job_id else str(uuid.uuid4())
        self.workspace = os.path.join(renderg_utils.get_workspace(workspace), _local_id)
        renderg_utils.check_path(self.workspace)

        self.info_path = os.path.join(self.workspace, "info.cfg")
        self.warning_path = os.path.join(self.workspace, "warning.json")

        self.warning_info = {}

    def add_warning(self, warn, *args):
        self.warning_info.update({warn.code(): warn.msg(*args)})
        renderg_utils.write_json(self.warning_path, self.warning_info)

    def check_file_version(self):
        regex = re.compile(r".*?Maya\s+ASCII\s+(?P<version>\d+(.\d)?)|.*?(?P<version_uver>\d{4}(.\d)?).*?UVER", re.IGNORECASE)
        version = renderg_utils.get_dcc_file_version(self.dcc_file, regex)
        if version != self.dcc_version:
            self.add_warning(WarnCode.DCCVersionNotMatchWarn, version, self.dcc_version)

    def find_dcc_exe(self):
        dcc_exe_path = ''
        local_dcc_exe_path = r"C:\Program Files\Autodesk\Maya{}\bin\mayabatch.exe".format(self.dcc_version)

        if os.path.isfile(local_dcc_exe_path):
            dcc_exe_path = local_dcc_exe_path
        else:

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Autodesk\Maya\{}\Setup\InstallPath'.format(self.dcc_version)
                )
                regedit_dcc_exe_path, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
                dcc_exe_path = os.path.join(regedit_dcc_exe_path, r'bin\mayabatch.exe')
            except BaseException as err:
                self.logger.warning(err.__str__())
        if not dcc_exe_path or not os.path.isfile(dcc_exe_path):
            raise DCCExeNotFoundError(ErrorCode.DCCExeNotFoundError, "Maya", self.dcc_version)

        return dcc_exe_path

    def analyze(self, cmd=None, env=None):
        self._update_analyze_status(JobStatus.STATUS_ANALYZE_DOING)

        self.check_file_version()
        if not self.dcc_exe_path:
            self.dcc_exe_path = self.find_dcc_exe()

        script_path = os.path.join(os.path.dirname(__file__), "maya/get_maya_infos.exe")
        if cmd is None:
            cmd = ('"{script_path}" --mayafile "{dcc_file}" --exepath "{dcc_exe_path}" '
                   '--proj "{project_path}" --jsonfile "{info_path}" --format json').format(
                script_path=script_path,
                dcc_file=self.dcc_file,
                info_path=self.info_path,
                dcc_exe_path=self.dcc_exe_path,
                project_path=self.project_path,
            )

        self.logger.info("Running command: {}".format(cmd))

        code, stderr = renderg_utils.run_cmd(cmd, shell=True, env=env)
        if code != 0:
            error_msg = stderr or "analyze exits unexpectedly"
            self._update_analyze_status(JobStatus.STATUS_ANALYZE_FAILED, error_msg)
            raise AnalyzeFailError(ErrorCode.AnalyzeFailError, error_msg)

        if not os.path.isfile(self.info_path):
            error_msg = "info.cfg not found. info_path=".format(self.info_path)
            self._update_analyze_status(JobStatus.STATUS_ANALYZE_FAILED, error_msg)
            raise AnalyzeFailError(ErrorCode.AnalyzeFailError, error_msg)

        self._update_analyze_status(JobStatus.STATUS_ANALYZED)
        return self

    def _update_analyze_status(self, status, msg=""):
        if self.job_id is None:
            return
        self.api.job.update_job_status(self.job_id, status, msg)
