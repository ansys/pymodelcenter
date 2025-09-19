# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# © 2025 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited
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

# Description: script loads workflow from specified path (workflowPath), allows user to set value for specified input variable (inputVar), run workflow, see result for specified output variable (outputVar), save workflow, and close workflow

from ansys.tools.variableinterop.scalar_values import RealValue
from ansys.tools.variableinterop.variable_state import VariableState

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

# initial variables
workflowPath = "C:\\Users\\joedward\\Documents\\MC\\brake\\brake.pxcz"
inputVar = "brake.caliper.pistonDiam"
outputVar = "brake.vehicle.stopDistance"

with grpcmc.Engine() as mc:
    print(f'\nLoading "{workflowPath}"..')

    # load existing workflow
    with mc.load_workflow(workflowPath) as workflow:

        # get state of workflow
        workflowState = workflow.get_state()
        print(f"- workflow loaded...state: {workflowState}")

        # get existing value of input variable
        inDatapin = workflow.get_datapin(inputVar)
        existingInVarVal = inDatapin.get_state().value
        print(f'- "{inputVar}" input variable value: {existingInVarVal}')

        # get existing value of output variable
        outDatapin = workflow.get_datapin(outputVar)
        existingOutVarVal = outDatapin.get_state().value
        print(f'- "{outputVar}" output variable value: {existingOutVarVal} \n')

        # prompt user for new input value and set in workflow
        newInVarValInput = RealValue(
            input(f'What value should "{inputVar}" have? ')
        )  # cast input as RealValue
        inDatapin.set_state(VariableState(newInVarValInput, True))

        # get state of output variable with new input variable set (should always be False)
        existingOutVarState = outDatapin.get_state().is_valid
        print(f'- "{outputVar}" output variable valid state: {existingOutVarState}')

        # run workflow
        workflow.run(collect_names=[outputVar])
        print("\nWorkflow ran..")

        # get new value of input variable
        newInVarVal = inDatapin.get_state().value
        print(f'- "{inputVar}" input variable value: {newInVarVal}')

        # get new value and state of output variable
        newOutVarVal = outDatapin.get_state().value
        newOutVarState = outDatapin.get_state().is_valid
        print(f'- "{outputVar}" output variable valid state: {newOutVarState}')
        print(f'- "{outputVar}" output variable value: {newOutVarVal} \n')

        # prompt user if workflow should be saved
        saveInput = input("Save workflow (y/n)? ")
        if saveInput in ["yes", "y"]:
            workflow.save_workflow()
            print("Workflow saved..")
        elif saveInput in ["no", "n"]:
            print("Workflow not saved..")
        else:
            print("Please enter 'y' or 'n'.")

        # pause until user presses any key, then close workflow
        exitInput = input("Done. Press any key to close the workflow and exit..")
        workflow.close_workflow()
