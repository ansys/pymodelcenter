"""Definition of DataExplorer."""
import clr

clr.AddReference(r"phoenix-mocks\Phoenix.Mock.v45")
import Phoenix.Mock as phxmock


class DataExplorer:
    """Container for trade study data (via a DataHistory) and plots."""

    def __init__(self, instance: phxmock.MockDataExplorer):
        self._instance = instance
