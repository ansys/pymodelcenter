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

# Description: script loads workflow from specified path (workflowPath), traverses the workflow for all variables and presents to the user, allows user to specify variables and values for modification, run workflow, see result for all variables, save workflow, and close workflow


from ansys.tools.variableinterop.scalar_values import RealValue
from ansys.tools.variableinterop.variable_state import VariableState

import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

# prompt user for full path to ModelCenter workflow PXCZ
workflowPath = input(
    "Enter the path to the ModelCenter workflow file (e.g., C:\\Users\\<username>\\Documents\\MC\\brake\\brake.pxcz): "
)
workflowElementsDict = {}


# function to traverse workflow for elements and their properties and values
def process_element(element, weDict):
    name = element.full_name
    is_component = isinstance(element, grpcmc.component.Component)
    is_control = isinstance(element, grpcmc.abstract_control_statement.AbstractControlStatement)
    is_group = isinstance(element, grpcmc.group.Group)
    if is_control:
        element_type = element.control_type
    elif is_group:
        element_type = "Group"
    elif is_component:
        element_type = "Component"
    else:
        element_type = "Unknown"

    if is_control:
        elements = element.get_elements()
        for key in elements.keys():
            process_element(elements[key], weDict)

    gr_map = element.get_groups()
    for key in gr_map.keys():
        process_element(gr_map[key], weDict)

    dp_map = element.get_datapins()
    for key in dp_map.keys():
        dp_name = dp_map[key].full_name
        is_input = dp_map[key].is_input_to_component
        dp_type = dp_map[key].value_type.to_display_string()
        dp_value = dp_map[key].get_state().value

        weDict[dp_name] = [is_input, dp_type, dp_value, key, name]
    return weDict


with grpcmc.Engine() as mc:
    print(f'\nLoading "{workflowPath}"..')

    # load existing workflow
    with mc.load_workflow(workflowPath) as workflow:
        # get root and state of workflow
        workflowRoot = workflow.get_root()
        workflowState = workflow.get_state()
        print(f"- workflow loaded")
        print(f"- workflow state: {workflowState}\n")

        # get initial workflow elements and their properties and values
        workflowElementsDict = process_element(workflowRoot, workflowElementsDict)
        print("Workflow elements:")
        print(workflowElementsDict)

        # prompt user for input variable and value that should be modified, then set in workflow
        # loop until user inputs "run" to execute the workflow
        while True:
            inVarInput = input(
                f'\nWhich input variable\'s value should be changed (format: model.component.variable, enter "run" to execute the workflow)? '
            )

            if inVarInput in workflowElementsDict:
                inDatapin = workflow.get_datapin(inVarInput)
                existingInVarVal = inDatapin.get_state().value
                print(f'- the existing value for "{inVarInput}" is: {existingInVarVal}')

                inVarValInput = RealValue(input(f'\nWhat new value should "{inVarInput}" have? '))
                inDatapin.set_state(VariableState(inVarValInput, True))

                workflowState = workflow.get_state()
                print(f"- workflow state: {workflowState}")
            elif inVarInput == "run":
                print("\nRunning workflow..")
                break
            else:
                print(
                    f'- "{inVarInput}" does not match the required format or is not a workflow variable, please try again..'
                )

        # run workflow
        workflow.run(collect_names=[])
        workflowState = workflow.get_state()
        print("- workflow ran")
        print(f"- workflow state: {workflowState}\n")

        # get executed workflow elements and their properties and values
        workflowElementsDict = process_element(workflowRoot, workflowElementsDict)
        print("Workflow elements:")
        print(workflowElementsDict)

        # prompt user if workflow should be saved
        saveInput = input("\nSave workflow (y/n)? ")
        if saveInput in ["yes", "y"]:
            workflow.save_workflow()
            print("- workflow saved\n")
        elif saveInput in ["no", "n"]:
            print("- workflow not saved\n")
        else:
            print("- please enter 'y' or 'n'")

        # pause until user presses any key, then close workflow
        exitInput = input("Press any key to close the workflow and exit..")
        workflow.close_workflow()
