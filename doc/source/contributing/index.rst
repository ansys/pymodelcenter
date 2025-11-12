.. _ref_contribute:

Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys developer's guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to Ansys ModelCenter Workflow.

The following contribution information is specific to Ansys ModelCenter Workflow.

Developer installation
-----------------------
Installing Ansys ModelCenter Workflow in developer mode allows you to modify the
source and enhance it. This package supports Python 3.10 through 3.13 on
Linux, macOS, and Windows.

For a local development version, you can create a clean virtual environment with
this command:

.. code:: bash

    python -m venv .venv

You can then activate the virtual environment with the command appropriate for
your operating system:

.. tab-set::

      .. tab-item:: Linux
        :sync: linux

        ::

          source .venv/bin/activate

      .. tab-item:: macOS
        :sync: macos

        ::

          source .venv/bin/activate

      .. tab-item:: Windows
        :sync: windows

        ::

          .\.venv\Scripts\activate

Next, install the development version of Ansys ModelCenter Workflow with
these commands:

.. code::

   git clone https://github.com/ansys/pymodelcenter
   cd pymodelcenter
   pip install -e .

Testing
-------
Once Ansys ModelCenter Workflow is installed in developer mode, install
the required dependencies for testing with this command:

.. code:: bash

    pip install -e .[tests]

To run the tests with `pytest <pytest_>`_, run
this command:

.. code:: bash

    pytest -v

To test and generate a code coverage report, run this command:

.. code::

    pytest tests/ --cov=ansys.modelcenter.workflow --cov-report=term --cov-report=html tests/

If a local copy of ModelCenter Desktop is installed and a local copy of
ModelCenter Remote Execution is installed and running, you can run the integration
tests with this command:

.. code::

    pytest integration

Documentation
-------------

To install the required dependencies for the documentation, run this command:

.. code::

    pip install .[doc]

To build documentation, run the usual rules provided in the
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ Makefile
for your operating system:

.. tab-set::

    .. tab-item:: Linux
      :sync: linux

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: macOS
      :sync: macos

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: Windows
      :sync: windows

      ::

        .\doc\make.bat html
        .\doc\_build\html\index.html

Post issues
-----------

Use the `Ansys ModelCenter Workflow Issues <pymodelcenter_issues_>`_ page to
report bugs and request new features. When possible, use the provided
templates. If your issue does not fit into one of these templates, click
the link for opening a blank issue.

If you have general questions about the PyAnsys ecosystem, email
`pyansys.core@ansys.com <pyansys.core@ansys.com>`_. If your
question is specific to Ansys ModelCenter Workflow, ask your
question in an issue as described in the previous paragraph.


Adhere to code style
--------------------

Ansys ModelCenter Workflow follows the PEP8 standard as indicated in
`PEP 8 <https://dev.docs.pyansys.com/coding-style/pep8.html>`_ in the 
*PyAnsys developer's guide* and implements style checking using
`pre-commit <pre-commit_>`_.

To ensure your code meets minimum code styling standards, run these commands:

.. code:: console

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command:

.. code:: console

  pre-commit install

This way, it's not possible for you to push code that fails the style checks:

.. code:: text

  $ git commit -am "added my cool feature"
  Add License Headers......................................................Passed
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  docformatter.............................................................Passed
  codespell................................................................Passed
  Validate GitHub Workflows................................................Passed
