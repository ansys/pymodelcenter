import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
import ansys.modelcenter.workflow.api as mcapi
import os

cwd = os.getcwd()
workflow_path = os.path.join(cwd, "ExampleProcess.pxcz")

print("Initializing workflow engine...")
with grpcmc.Engine() as mc:
   print("Creating workflow: " + workflow_path)
   with mc.new_workflow(workflow_path, mcapi.WorkflowType.PROCESS) as workflow:
      print("Creating quadratic...")
      workflow.create_component(
         server_path="common:\\Functions\\Quadratic",
         name="NewQuadratic",
         parent="Model"
      )
      
      print("Running...")
      workflow.run(validation_names={"Model.NewQuadratic.y"})
      
      print("Saving...")
      workflow.save_workflow()
      
      print("Done.")
