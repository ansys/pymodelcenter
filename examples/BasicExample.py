#############################################################
# Simple introduction to ansys.tools.variableinterop
#
# Shows how to set values using workflow.set_value(), and how
# to get values from datapins
#############################################################
from ansys.modelcenter.workflow.grpc_modelcenter import Engine
from ansys.tools.variableinterop.scalar_values import RealValue
import os

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
