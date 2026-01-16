# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

# Description:
# creates a new workflow with an Optimization Tool component and Quadratic component
# nested under it. It then configures and runs the optimization

import os
from ansys.tools.variableinterop.scalar_values import RealValue
from ansys.tools.variableinterop.scalar_values import StringValue
from ansys.tools.variableinterop.variable_state import VariableState
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
import ansys.modelcenter.workflow.api as mcapi

# create workflow relative to script
cwd = os.getcwd()
workflow_path = os.path.join(cwd, "Optimization.pxcz")

# contant value to assign to a variable not used in optimization design variables
newConstantVal = 3

with grpcmc.Engine() as mc:    
    with mc.new_workflow(workflow_path, mcapi.WorkflowType.PROCESS) as workflow:
        print("\n- workflow created: " + workflow_path)
        
        # get workflow root element
        workflowRoot = workflow.get_root()
        
        # create Opt Tool component        
        optComp = workflow.create_component(
            "component plug-in:SOFTWARE\\Phoenix Integration\\"
            "Component Plug-Ins\\Optimization Tool",
            "Optimization",
            workflowRoot,
        )
        print("- Optimization component created")

        # create Quadratic component under Opt Tool component 
        targetComp = workflow.create_component(
            "common:\\Functions\\Quadratic", 
            "Quadratic", 
            optComp
        )
        print("- Quadratic component created under Optimization component")
        
        # get existing hardcoded datapin values and states
        inVarName = targetComp.full_name + ".x"
        extraInVarName = targetComp.full_name + ".c"
        outVarName = targetComp.full_name + ".y"
        inDatapin = workflow.get_datapin(inVarName)
        extraInDatapin = workflow.get_datapin(extraInVarName)
        outDatapin = workflow.get_datapin(outVarName)
        print(f'- existing value for {inVarName}: {inDatapin.get_state().value} ' 
            f'(valid={inDatapin.get_state().is_valid})')
        print(f'- existing value for {outVarName}: {outDatapin.get_state().value} ' 
            f'(valid={outDatapin.get_state().is_valid})')

        # set additional input variable that isn't an optimization design variable 
        # to new value
        extraInDatapin.set_state(VariableState(RealValue(newConstantVal), True))
        print(f'- new value for {extraInVarName} set to: {extraInDatapin.get_state().value} '
            f'(valid={extraInDatapin.get_state().is_valid})')
        
        # set Opt Tool component datapins
        algorithmDatapin = optComp.get_datapins()["algorithm"]
        algorithmDatapin.set_state(VariableState("com.ansys.osl_algorithm.NLPQLP", True))
        print(f'\n- algorithm set to "Optislang NLPQLP algorithm"')
        
        objectiveDatapin = optComp.get_datapins()['objectives'] 
        objectiveDatapin.set_length(1)
        objectiveDatapin[0].equation = outVarName  
        print(f'- objective set to "{objectiveDatapin[0].equation}"')
        
        objective_refProps = objectiveDatapin.get_reference_properties()
        objective_refProps["goal"].set_value_at(0, VariableState("solveFor", True))
        print(f'- objective goal set to "solveFor: 0"')
        
        contDesignVars = optComp.get_datapins()["continuousDesignVariables"]
        contDesignVars.set_length(1)
        contDesignVars[0].equation = inVarName 
        print(f'- continuous design variable set to "{contDesignVars[0].equation}"')
        
        contDesignVars_refProps = contDesignVars.get_reference_properties()
        contDesignVars_refProps["startValue"].set_value_at(0, VariableState(StringValue("5.0"), True))
        contDesignVars_refProps["lowerBound"].set_value_at(0, VariableState(RealValue(-10.0), True))
        contDesignVars_refProps["upperBound"].set_value_at(0, VariableState(RealValue(10.0), True))
        print(f'- continuous design variable bound values set')

        # run workflow
        print("\nRunning workflow..")
        workflow.run(validation_names={optComp.full_name + ".optimizationToolReturnStatus"})
        
        # get output values and states
        optToolReturnStatusDatapin = optComp.get_datapins()['optimizationToolReturnStatus']
        if optToolReturnStatusDatapin.get_state().value == 10:
            print(f'\n- optimization tool return status: Successful Convergence')
        else:
            print(f'\n- optimization tool return status: {optToolReturnStatusDatapin.get_state().value}')

        print(f'- new value for {inVarName}: {inDatapin.get_state().value} '
            f'(valid={inDatapin.get_state().is_valid})')
        print(f'- new value for {outVarName}: {outDatapin.get_state().value} ' 
            f'(valid={outDatapin.get_state().is_valid})')        
        
        # prompt user if workflow should be saved
        saveInput = input("\nSave workflow (y/n)? ")
        if saveInput in ["yes", "y"]:
            workflow.save_workflow()
            print("- workflow saved")
        elif saveInput in ["no", "n"]:
            print("- workflow will not be saved")
        else:
            print("Please enter 'y' or 'n'.")   #needs refactor

        # pause until user presses any key, then close workflow
        exitInput = input("\nPress any key to close the workflow and exit..")        
        workflow.close_workflow()
        if saveInput in ["no", "n"]:
            os.remove(workflow_path)