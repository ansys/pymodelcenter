#############################################################
# Inserting new components, linking datapins
#
# Shows how to add a second quadratic component, and link
# selected datapins from each component together
#############################################################
from ansys.modelcenter.workflow.grpc_modelcenter import Engine
import os

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
            server_path="common:\\Functions\\Quadratic",
            name="B",
            parent="Model"
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
