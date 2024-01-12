from typing import Union


class Data:
    def __init__(self, data: dict = dict()):
        self._data = data


class MediaData(Data):
    def __init__(self, file_path, metadata=None, ffmpeg_params=None):
        _data = {
            "file_path": file_path,
            "metadata": metadata,
            "ffmpeg_params": ffmpeg_params
        }
        super().__init__(_data)
        self.file_path = self._data.get(file_path)
        self.metadata = self._data.get(metadata)
        self.ffmpeg_params = self._data.get(ffmpeg_params)


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