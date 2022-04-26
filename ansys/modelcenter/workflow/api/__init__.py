
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from .engine import Engine
from .ui_configure_workflow import UIConfigureWorkflow
from .workflow import Workflow
