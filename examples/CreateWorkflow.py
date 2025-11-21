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

"""Create a new workflow in Ansys ModelCenter Workflow."""

import os

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

cwd = os.getcwd()
workflow_path = os.path.join(cwd, "ExampleProcess.pxcz")

print("Initializing workflow engine...")
with grpcmc.Engine() as mc:
    print("Creating workflow: " + workflow_path)
    with mc.new_workflow(workflow_path, mcapi.WorkflowType.PROCESS) as workflow:
        print("Creating quadratic...")
        workflow.create_component(
            server_path="common:\\Functions\\Quadratic", name="NewQuadratic", parent="Model"
        )

        print("Running...")
        workflow.run(validation_names={"Model.NewQuadratic.y"})

        print("Saving...")
        workflow.save_workflow()

        print("Done.")
