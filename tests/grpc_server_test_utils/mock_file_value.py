from os import PathLike
from typing import Optional

import ansys.tools.variableinterop as atvi


class MockFileValue(atvi.FileValue):
    def __init__(self, path: Optional[str] = None) -> None:
        super(MockFileValue, self).__init__(
            original_path=path, value_id=None, encoding=None, mime_type=None
        )

    @property
    def actual_content_file_name(self) -> Optional[PathLike]:
        return self._original_path

    def _has_content(self) -> bool:
        return self._original_path is not None

    def __eq__(self, other) -> bool:
        return isinstance(other, MockFileValue) and other._original_path == self._original_path
