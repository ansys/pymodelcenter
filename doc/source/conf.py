"""Sphinx documentation configuration file."""
from datetime import datetime
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath("../.."))

from ansys_sphinx_theme import (
    ansys_favicon,
    ansys_logo_white,
    ansys_logo_white_cropped,
    get_autoapi_templates_dir_relative_path,
    get_version_match,
    latex,
    pyansys_logo_black,
    watermark,
)

from ansys.modelcenter.workflow import __version__

# Project information
project = "ansys-modelcenter-workflow"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "Ansys, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "modelcenter.docs.pyansys.com")
switcher_version = get_version_match(__version__)

REPOSITORY_NAME = "pymodelcenter"
USERNAME = "pyansys"
BRANCH = "main"
DOC_PATH = "doc/source"

# use the default ansys logo
html_logo = pyansys_logo_black
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyAnsys ModelCenter Workflow"

# specify the location of your github repo
html_theme_options = {
    "github_url": f"https://github.com/ansys/{REPOSITORY_NAME}",
    "check_switcher": False,
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": switcher_version,
    },
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": f"https://github.com/ansys/{REPOSITORY_NAME}/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": USERNAME,
    "github_repo": REPOSITORY_NAME,
    "github_version": BRANCH,
    "doc_path": DOC_PATH,
}

# Sphinx extensions
extensions = [
    "notfound.extension",  # for the not found page.
    "numpydoc",
    "autoapi.extension",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "grpc": ("https://grpc.github.io/grpc/python/", None),
    "pypim": ("https://pypim.docs.pyansys.com/version/stable/", None),
    "ansys.engineeringworkflow.api": (
        "https://engineeringworkflow.docs.pyansys.com/version/stable/",
        None,
    ),
    "ansys.tools.varaibleinterop": (
        "https://variableinterop.docs.pyansys.com/version/stable/",
        None,
    ),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_xref_param_type = True
autosectionlabel_prefix_document = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
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

# Favicon
html_favicon = ansys_favicon

exclude_patterns = ["ansys/modelcenter/workflow/grpc_modelcenter/proto*"]

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Configuration for Sphinx autoapi
autoapi_type = "python"
autoapi_dirs = ["../../src/ansys/"]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
]
autoapi_template_dir = get_autoapi_templates_dir_relative_path(Path(__file__))
suppress_warnings = ["autoapi.python_import_resolution"]
autoapi_python_use_implicit_namespaces = True
autoapi_render_in_single_page = ["class", "enum", "exception"]
autoapi_own_page_level = "class"
autoapi_ignore = ["*_visitors*"]
autoapi_keep_files = True

# Generate section labels up to four levels deep
autosectionlabel_maxdepth = 4

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "links.rst",
]

linkcheck_ignore = [
    "https://github.com/ansys/pymodelcenter/*",  # this site is private
    "https://modelcenter.docs.pyansys.com//*",  # this site is private
]

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"{project}-Documentation-{__version__}.tex",
        f"{project} Documentation",
        author,
        "manual",
    ),
]

# additional logos for the latex coverpage
latex_additional_files = [watermark, ansys_logo_white, ansys_logo_white_cropped]

# change the preamble of latex with customized title page
# variables are the title of pdf, watermark
latex_elements = {"preamble": latex.generate_preamble(html_title)}
sd_fontawesome_latex = True
