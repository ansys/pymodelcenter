.. _ref_user_guide:

User guide
==========

The main classes used to create and run workflows are the ``Engine``
and ``Workflow`` classes.

This code shows how to create a workflow, add a component to it,
run it, and then save it:

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
