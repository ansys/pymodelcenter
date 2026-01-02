# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

#############################################################
# Inserting new components, linking datapins
#
# Shows how to add a second quadratic component, and link
# selected datapins from each component together
#############################################################
from ansys.modelcenter.workflow.grpc_modelcenter import Engine

cwd = os.getcwd()
workflow_filename = "BasicExample.pxcz"
workflow_path = os.path.join(cwd, workflow_filename)

print("Initializing workflow engine...")
with Engine() as mc:
    print("Loading workflow: " + workflow_path)
    with mc.load_workflow(workflow_path) as workflow:
        print("Loaded: " + workflow_filename)

        # when you create a component in a process workflow, the default
        # behavior is to put it at the end of its parent sequence
        print("Creating a new component...")
        quadB = workflow.create_component(
            server_path="common:\\Functions\\Quadratic", name="B", parent="Model"
        )

        print("Getting datapin...")
        b_xDatapin = quadB.get_datapins()["x"]

        # create a link between Model.Quadratic.y and Model.B.x
        # the "datapin" parameter of this method accepts either a string naming
        # the element or a reference to the datapin object. Likewise, the
        # "equation" parameter can be either a link equation string or a datapin reference
        print("Creating links...")
        workflow.create_link(datapin=b_xDatapin, equation="Model.Quadratic.y")

        print("Saving workflow to ExampleWithLinks.pxcz...")
        workflow.save_workflow_as(os.path.join(cwd, "ExampleWithLinks.pxcz"))
