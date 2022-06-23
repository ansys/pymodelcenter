"""
Ansys ModelCenter Workflow.

--------------------------

This library provides a Python API for using the ModelCenter suite of
Ansys products. These products provide tools for creating and automating
engineering workflows.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
