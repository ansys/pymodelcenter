PyAnsys ModelCenter Workflow
############################
|pyansys| |python| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/Python-%3E%3D3.8-blue
   :target: https://pypi.org/project/py-cam-client/
   :alt: Python

.. TODO: pypi and GH-CI badges

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code_style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


Project Overview
----------------
This library provides a Python API for using the ModelCenter suite of
Ansys products. These products provide tools for creating and automating
engineering workflows.


Installation
------------
The ``ansys-modelcenter-workflow`` package currently supports Python
3.8 through 3.10 on Windows.
This package is not currently available on PyPI, but will be when it is
ready for use.
At that time you can install ``ansys-modelcenter-workflow`` with:

.. code::

   pip install ansys-modelcenter-workflow

Alternatively, install the latest development version directly from
the `pymodelcenter GitHub <https://github.com/ansys/pymodelcenter>`_ via:

.. code::

   pip install git+https://github.com/ansys/pymodelcenter.git

For a local "development" version, install with:

.. code::

   git clone https://github.com/ansys/pymodelcenter.git
   cd pymodelcenter
   pip install poetry
   poetry install -E dev

This creates a new virtual environment, which can be activated with:

.. code::

   poetry shell

The grpc proto files needed to build can then be generated using the generate-proto batch script
in ./protos.


Documentation
-------------
`API Documentation <api/index.html>`_

For building documentation, you can run the usual rules provided in the Sphinx Makefile.
First, ensure the required dependencies are installed with:

.. code::

    poetry install -E docs

Then on Unix run:

.. code::

    make -C doc/ html && your_browser_name doc/html/index.html

and on Windows run:

.. code::

    .\doc\make.bat html



Usage
-----
The main classes used to create and run workflows are the ``Engine`` class
and the ``Workflow`` class.

This is an example of how to load a previously saved workflow, execute
it, and retrieve the value of a variable:

.. code:: python

    import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

    with grpcmc.Engine() as mc:
        print("Creating new model...")
        with mc.new_workflow("d:\\workspace\\Designs\\DEMO\\demo.pxcz") as workflow:
            root_id = workflow.get_root().element_id

            print("     Directory: " + workflow.workflow_directory)
            print("          File: " + workflow.workflow_file_name)

            workflow.create_component(
                "common:\\Functions\\Quadratic",
                "NewQuadratic",
                root_id,
                x_pos=50, y_pos=50)

            print("Saving...")
            workflow.save_workflow()
            print("Done.")

Testing
-------
Dependencies required for testing can be installed via:

.. code::

    poetry install -E test

The tests can then be run via pytest. To test and generate a code coverage report run:

.. code::

    pytest tests/ --cov=ansys.modelcenter.workflow --cov-report=term --cov-report=html tests/

If a local copy of ModelCenter Desktop is installed, and a local copy of ModelCenter Remote Execution is installed and running, the integration tests can be run with:

    pytest integration/

License
-------
ansys-modelcenter-workflow is licensed under the MIT license.

