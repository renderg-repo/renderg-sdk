from enum import Enum


class WarnCode(Enum):
    DCCVersionNotMatchWarn = ("000000", "dcc version not match. your version: {}, file version: {}")

    def code(self):
        return self.value[0]

    def msg(self, *args):
        return self.value[1].format(*args)


class ErrorCode(Enum):
    DCCFileNotExistsError = ("000000", "{} is not exist!")
    DCCExeNotFoundError = ("000001", "{} {} not found locally!")
    MayaProjectInvalidError = ("000100", "Maya project {} not found locally!")
    AnalyzeFailError = ("000002", "{}")
    AssetUploadFailError = ("000003", "asset upload failed. ascp return code: {}")

    def code(self):
        return self.value[0]

    def msg(self, *args):
        return self.value[1].format(*args)


class RenderGException(Exception):

    def __init__(self, error: 'ErrorCode', *args):
        self.err_code = error.code()
        self.err_msg = error.msg(*args)

    def __str__(self):
        return "Error code:{}, Error message:{}".format(self.err_code, self.err_msg)


class DCCFileNotExistsError(RenderGException):
    '''DCCExeNotFoundError'''


class DCCExeNotFoundError(RenderGException):
    '''DCCExeNotFoundError'''


class AnalyzeFailError(RenderGException):
    '''DCCExeNotFoundError'''


class AssetUploadError(RenderGException):
    """资产上传失败异常，包含 ascp 返回码和排查所需的文件路径。"""

    def __init__(self, return_code, stderr="", pair_file="", ascp_log_dir="", run_dir=""):
        super(AssetUploadError, self).__init__(ErrorCode.AssetUploadFailError, return_code)
        self.return_code = return_code
        self.stderr = stderr or ""
        self.pair_file = pair_file or ""
        self.ascp_log_dir = ascp_log_dir or ""
        self.run_dir = run_dir or ""

    def __str__(self):
        return "{}; return_code={}, stderr={}, pair_file={}, ascp_log_dir={}, run_dir={}".format(
            super(AssetUploadError, self).__str__(),
            self.return_code,
            self.stderr,
            self.pair_file,
            self.ascp_log_dir,
            self.run_dir,
        )
