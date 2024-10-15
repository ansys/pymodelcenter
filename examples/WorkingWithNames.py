##############################################
# Working with element names (getting elements, renaming)
#
# Most elements are subclassed from AbstractRenamableElement
# Datapins and Groups are the notable exceptions
###############################################
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

        # the methods on Workflow expect the full name to the element
        quadratic = workflow.get_element_by_name("Model.Quadratic")

        # but the methods on elements use the "local" name for that element
        quadratic.rename("A")
        print("We have renamed Model.Quadratic to " + quadratic.full_name)

        # we have renamed Quadratic, so it is no longer accessible by that full name
        elementA = workflow.get_element_by_name("Model.A")

        # but it should still refer to the same element object
        areSame = quadratic == elementA
        print("Do <quadratic> and <elementA> objects refer to the same element?   " + ("Yes!" if areSame else "No!"))
