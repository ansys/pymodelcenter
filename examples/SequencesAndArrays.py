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

############################################
# Example of how to create new sequences and arrays
############################################
import os

from ansys.tools.variableinterop.variable_state import VariableState
from ansys.tools.variableinterop.variable_type import VariableType
import numpy as np

import ansys.modelcenter.workflow.api as mcapi
from ansys.modelcenter.workflow.api.iassembly import AssemblyType
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

cwd = os.getcwd()
workflow_filename = "ExampleSequence.pxcz"
workflow_path = os.path.join(cwd, workflow_filename)

print("Initializing workflow engine...")
with grpcmc.Engine() as mc:
    print("Loading workflow: " + workflow_path)
    with mc.new_workflow(workflow_path, mcapi.WorkflowType.PROCESS) as workflow:
        print("Loaded: " + workflow_filename)

        print("Creating sequences...")
        root: grpcmc.Assembly = workflow.get_root()
        pAssembly = workflow.create_assembly(
            name="NewSequence", parent=root, assembly_type=AssemblyType.SEQUENCE
        )

        rAssembly = workflow.create_assembly(
            name="ResultSequence", parent=root, assembly_type=AssemblyType.SEQUENCE
        )

        aValue = np.float64([1.0, 2.0, 3.0])
        bValue = np.float64([4.0, 5.0, 6.0])
        cross_product = np.cross(aValue, bValue)
        dot_product = np.dot(aValue, bValue)

        # create a and b array variables inside M, and set values
        # from the numpy arrays we created earlier
        print("Add datapin array1 to sequence P...")
        adp = pAssembly.add_datapin("array1", VariableType.REAL_ARRAY)
        adp.set_state(VariableState(aValue, True))

        print("Add datapin array2 to sequence P...")
        bdp = pAssembly.add_datapin("array2", VariableType.REAL_ARRAY)
        bdp.set_state(VariableState(bValue, True))

        print("Add datapin cross_product to sequence P...")
        cpdp = pAssembly.add_datapin("cross_product", VariableType.REAL_ARRAY)
        cpdp.set_state(VariableState(cross_product, True))

        print("Add datapin dot_product to sequence P...")
        dpdp = pAssembly.add_datapin("dot_product", VariableType.REAL)
        dpdp.set_state(VariableState(dot_product, True))

        print("Add datapin y to sequence R...")
        ydp = rAssembly.add_datapin("y", VariableType.REAL_ARRAY)
        ydp.set_state(VariableState(cross_product, True))

        print("Add datapin z to sequence R...")
        zdp = rAssembly.add_datapin("z", VariableType.REAL)
        zdp.set_state(VariableState(dot_product, True))

        workflow.create_link(ydp, cpdp)
        workflow.create_link(zdp, dpdp)

        print("Running...")
        workflow.run()

        print("The cross product and dot product on R are:")
        print(" ==>[" + ydp.name + "] : " + str(ydp.get_state().value))
        print(" ==>[" + zdp.name + "] : " + str(zdp.get_state().value))

        print("Saving...")
        workflow.save_workflow()

        print("Done.")
