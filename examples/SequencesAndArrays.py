############################################
# Example of how to create new sequences and arrays
############################################
import os

import numpy as np
from ansys.tools.variableinterop.variable_state import VariableState
from ansys.tools.variableinterop.variable_type import VariableType

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
from ansys.modelcenter.workflow.api.iassembly import AssemblyType

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
            name="NewSequence",
            parent=root,
            assembly_type=AssemblyType.SEQUENCE)

        rAssembly = workflow.create_assembly(
            name="ResultSequence",
            parent=root,
            assembly_type=AssemblyType.SEQUENCE)

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
