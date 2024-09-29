import os
from pathlib import Path
from typing import Union


class DirectoryLocation:
    def __init__(self, source: Union[str, Path]):
        source_path = Path(source)
        if source_path.exists() and not source_path.is_dir():
            raise NotADirectoryError(f"Path exists but is not a directory: {source_path}")
        if not source_path.is_dir() and not os.path.exists(source_path):
            print(f"Path does not exist. Creating directory: {source_path}")
            os.makedirs(source_path)
        self._source = source_path

    @property
    def source(self) -> Path:
        return self._source


class DocumentLocation(DirectoryLocation):
    def __init__(self, source: Union[str, Path], filename: str):
        super().__init__(source)
        self._filename = filename

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def full_path(self) -> Path:
        return self.source / self.filename

    @property
    def get_directory_location(self) -> DirectoryLocation:
        return DirectoryLocation(self.source)
