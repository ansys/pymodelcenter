"""This init file allows python to treat directories containing it as modules.

Import any methods you want exposed at your library level here.

For example, if you want to avoid this behavior:

.. code::

   >>> from ansys.modelcenter.api.module import add

Then add the import within this module to enable:

.. code::

   >>> from ansys.modelcenter import api
   >>> api.add(1, 2)

.. note::
   The version is obtained from the installation metadata. During development,
   it will only update after re-executing `poetry install`.

"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from ansys.modelcenter.api.module import add
from ansys.modelcenter.api.other_module import Complex
