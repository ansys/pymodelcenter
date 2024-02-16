# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import PathLike
from typing import Optional

import ansys.tools.variableinterop as atvi


class MockFileValue(atvi.LocalFileValue):
    def __init__(self, path: Optional[str] = None) -> None:
        super(MockFileValue, self).__init__(
            original_path=path,
            value_id=None,
            encoding=None,
            mime_type=None,
            actual_content_file_name=path,
        )

    @property
    def actual_content_file_name(self) -> Optional[PathLike]:
        return self._original_path

    def _has_content(self) -> bool:
        return self._original_path is not None

    def __eq__(self, other) -> bool:
        return isinstance(other, MockFileValue) and other._original_path == self._original_path
