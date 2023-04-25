"""Sphinx documentation configuration file."""
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from ansys_sphinx_theme import get_version_match
from ansys_sphinx_theme import pyansys_logo_black as logo

from ansys.modelcenter.workflow import __version__

# Project information
project = "ansys-modelcenter-workflow"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "Ansys, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "nocname.com")

# use the default ansys logo
html_logo = logo
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "ansys-modelcenter-workflow"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/pyansys/pymodelcenter",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "numpy": ("https://numpy.org/devdocs", None),
}

# options affecting autodoc generation
autosummary_generate = True
add_module_names = False

autodoc_default_options = {"autodoc_typehints_format": "short", "autodoc_typehints": "description"}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    "SS03",  # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    "SS05",  # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned
}

exclude_patterns = ["ansys/modelcenter/workflow/grpc_modelcenter/proto*"]

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Generate section labels up to four levels deep
autosectionlabel_maxdepth = 4
