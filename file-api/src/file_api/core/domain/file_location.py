class FileLocation:
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
