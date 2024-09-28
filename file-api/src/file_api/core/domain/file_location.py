from pathlib import Path




class DirectoryLocation:
    def __init__(self, source: str):
        if not Path(source).is_dir():
            raise ValueError(f"The provided location {source} is not a valid directory.")

        self._source = source

    @property
    def source(self) -> str:
        return self._source


class DocumentLocation:
    def __init__(self, source: str, filename: str):
        self._source = source
        self._filename = filename

    @property
    def source(self) -> str:
        return self._source

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def full_path(self) -> str:
        return f"{self.source}/{self.filename}"

    @property
    def get_dir_location(self) -> DirectoryLocation:
        return DirectoryLocation(self.source)
