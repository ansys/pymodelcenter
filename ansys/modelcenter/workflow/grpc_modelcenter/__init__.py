"""
This package provides a gRPC-based implementation of the ModelCenter Python API.

This implementation will find a local installation of ModelCenter, launch it,
and attempt to communicate with it via gRPC.
"""

from .engine import Engine
from .workflow import Workflow
