.. _ref_user_guide:

User guide
==========

To create and run workflows, you use Ansys ModelCenter Workflow's 
main ``Engine`` and ``Workflow`` classes.

This code shows a simple example of how to create a workflow, add a
component to it, run it, and then save it:

.. code:: python

    import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

    with grpcmc.Engine() as mc:
        print("Creating workflow...")
        with mc.new_workflow("d:\\example.pxcz") as workflow:
            print("Creating quadratic...")
            workflow.create_component(
                server_path="common:\\Functions\\Quadratic",
                name="NewQuadratic",
                parent="Model",
            )

            print("Running...")
            workflow.run(validation_names=["Model.NewQuadratic.y"])

            print("Saving...")
            workflow.save_workflow()

            print("Done.")

For more detailed user cases check the files in the /examples folder.