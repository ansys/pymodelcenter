"""
Ansys ModelCenter Desktop
----------------------------

Python interface for automating ModelCenter Desktop.

ModelCenter Desktop is a Windows COM application for automating
execution of engineering workflows.

Examples
--------
Printing the version of the application:
instance = ModelCenter()
version = instance.version
print(version)

LTTODO: any other examples or notes that would help users
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from ansys.modelcenter.desktop.modelcenter import ModelCenter
