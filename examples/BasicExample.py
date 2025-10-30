# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Basic example of using the Ansys ModelCenter Workflow API."""

import os

from ansys.tools.variableinterop.scalar_values import RealValue

#############################################################
# Simple introduction to ansys.tools.variableinterop
#
# Shows how to set values using workflow.set_value(), and how
# to get values from datapins
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

        x_reference = workflow.get_datapin("Model.Quadratic.x").get_state().value
        print("Reference x value: " + str(x_reference))

        x_value = RealValue(123.0)
        print("Setting x to: " + str(x_value))
        workflow.set_value("Model.Quadratic.x", x_value)

        print("Running workflow...")
        workflow.run()

        x_value_new = workflow.get_datapin("Model.Quadratic.x").get_state().value
        print("x value is now: " + str(x_value_new))

        y_value = workflow.get_datapin("Model.Quadratic.y").get_state().value
        print("y value is now: " + str(y_value))
