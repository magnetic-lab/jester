from typing import Union


class Data:
    def __init__(self, data: dict = dict()):
        self._data = data

    @property
    def data(self):
        return self._data


class MediaData(Data):
    def __init__(self, file_path=None):
        data = {
            "file_path": file_path
        }
        super().__init__(data)
    
    @property
    def file_path(self):
        return self.data.get("file_path")

    @file_path.setter
    def file_path(self, value):
        self.data["file_path"] = value

    @property
    def metadata(self):
        return self.data.get("metadata")

    @metadata.setter
    def metadata(self, value):
        self.data["metadata"] = value

    @property
    def ffmpeg_params(self):
        return self.data.get("ffmpeg_params")

    @ffmpeg_params.setter
    def ffmpeg_params(self, value):
        self.data["ffmpeg_params"] = value


class JSONData(Data):
    def __init__(self, data: dict = dict()):
        super().__init__(data)


class YAMLData(Data):
    def __init__(self, data: dict = dict()):
        super().__init__(data)


class TextData(Data):
    def __init__(self, text: Union[bytes, str] = ""):
        if isinstance(text, bytes):
            text = text.decode()
        _data = {
            "text": text
        }
        super().__init__(_data)