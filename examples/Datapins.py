# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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
"""Datapins example for Ansys ModelCenter Workflow."""

import os

from ansys.tools.variableinterop.scalar_values import RealValue
from ansys.tools.variableinterop.variable_state import VariableState
from ansys.tools.variableinterop.variable_value import VariableValueInvalidError
import numpy as np

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

cwd = os.getcwd()
workflow_filename = "BasicExample.pxcz"
workflow_path = os.path.join(cwd, workflow_filename)

print("Initializing workflow engine...")
with grpcmc.Engine() as mc:
    print("Loading workflow: " + workflow_path)
    with mc.load_workflow(workflow_path) as workflow:
        print("Loaded: " + workflow_filename)

        # working with RealValue, IntegerValue, and StringValue are straightforward if you
        # use Numpy float64 / int / str dtype with them. You can perform normal pythonic
        # calculations and assignments this way
        a = np.float64(1.5)
        newXValue = RealValue(3.0)
        newXValue *= a
        print("Setting x value to " + str(newXValue))
        # actually setting the value in the MC workflow datapin can involve a few steps.
        #
        # method a) if you have quick access to the workflow object you can use the shortcut method
        # workflow.set_value(full_name, value)
        workflow.set_value("Model.Quadratic.x", newXValue)

        # method b) if you are accessing the datapin, call set_state() with a VariableState object.
        # VariableState is a class than combines the value with valid/invalid status of the variable
        #
        x = workflow.get_datapin("Model.Quadratic.x")
        x.set_state(VariableState(newXValue, True))
        workflow.run()

        # getting output variable
        y = workflow.get_datapin("Model.Quadratic.y")

        # IDatapin.get_state() returns a VariableState object
        # VariableState object has three properties:
        # 1) is_valid: it indicates if the value has been calculated in MC using the most recent
        #    input values
        # 2) value
        # 3) safe_value
        # The difference between 2) and 3) is that if you try to access safe_value before the
        # workflow has been run/updated,
        # you will raise a VariableValueInvalidError. The value property will always return the
        # current value regardless whether it is valid or not.

        y_display_value = y.get_state().value.to_display_string("fr_FR")
        y_is_valid = y.get_state().is_valid
        y_value = y.get_state().value
        # y_safe_value    = y.get_state().safe_value
        print("y value using French locale str conversion: " + y_display_value)
        print("y's validity status is " + ("valid" if y_is_valid else "invalid"))
        print("y value using default locale str conversion: " + str(y_value))

        print("Updating x value to 2.6")
        workflow.set_value("Model.Quadratic.x", 2.6)

        print("y's validity status is now " + ("valid" if y.get_state().is_valid else "invalid"))
        print("getting y.get_state().safe_value should throw an error: ", end="")

        try:
            print(str(y.get_state().safe_value))
        except VariableValueInvalidError:
            print("VariableValueInvalidError caught!")

        print("Running the workflow once more to recalculate y")
        workflow.run()
        print("For x= " + str(x.get_state().value) + " our new y= " + str(y.get_state().value))
        print("and y's validity status is now ", ("valid" if y.get_state().is_valid else "invalid"))
