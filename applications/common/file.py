import os

from flask import request


def get_file_size(file_path):
    return get_readable_size(os.path.getsize(file_path))


def get_readable_size(f_size):
    if f_size < 1024:
        return str(f_size) + "Byte"
    else:
        kbx = f_size / 1024
        if kbx < 1024:
            return str(round(kbx, 2)) + "K"
        else:
            mbx = kbx / 1024
            if mbx < 1024:
                return str(round(mbx, 2)) + "M"
            else:
                return str(round(mbx / 1024)) + "G"


class ExistsError(Exception):
    ...


class UploadError(Exception):
    ...


class ChunkOptions:

    def __init__(self, _on_finished=None):
        self.total_chunks = None
        self.offset = None

        self.chunk_block = None
        self.chunk_id = None

        self.file_id = None
        self.file_name = None
        self.file_size = None

        self._on_finished = _on_finished

        self.url_prefix = "/static/"

    @staticmethod
    def from_flask_request(_on_finished=None):
        options = ChunkOptions(_on_finished)

        options.total_chunks = int(request.form["totalChunks"])  # 总计块数量
        options.offset = int(request.form["offset"])  # 文件偏移位置

        options.chunk_block = request.files["chunkBlock"]  # 当前块内容
        options.chunk_id = int(request.form["chunkID"])  # 当前块编号

        options.file_id = request.form["fileID"]  # 块存储唯一ID
        options.file_name = request.form["fileName"]  # 文件原始名称
        options.file_size = int(request.form["fileSize"])  # 文件原始总大小

        return options

    def is_end_block(self):
        """

        判定当前块是否为最终块

        :return:

        """
        return self.chunk_id + 1 == self.total_chunks

    def render_url(self):
        return f"{self.url_prefix}{self.file_name}"

    def on_process(self, result, save_path):
        """

        进程块保存完毕时回调处理

        :param save_path:
        :param result:
        :return:

        """
        pass

    def on_finished(self, result, save_path):
        """

        最终块保存完毕时回调处理

        :param save_path:
        :param result:
        :return:

        """
        if callable(self._on_finished):
            self._on_finished(self, result, save_path)


class SliceSaveFile:

    def __init__(self, options: ChunkOptions):
        self.options = options
        self.save_path = f"static/{options.file_name}"

    def is_exists(self):
        if os.path.exists(self.save_path) and self.options.chunk_id == 0:
            return True
        return False

    def save(self):
        if self.is_exists():
            raise ExistsError("文件已经存在")

        with open(self.save_path, "ab") as f:
            f.seek(self.options.offset)
            f.write(self.options.chunk_block.stream.read())

        result = {
            "name": self.options.file_name,
            "url": self.options.render_url(),
            "uid": self.options.file_id,
            "status": "success"
        }

        if self.options.is_end_block():
            if os.path.getsize(self.save_path) != self.options.file_size:
                raise UploadError("上传失败")
            self.options.on_finished(result, self.save_path)
        else:
            self.options.on_process(result, self.save_path)

        return result
