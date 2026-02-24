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
# Creates a new 'FileVariables.pxcz' Process workflow with:
# - an 'InputFile_Assembly' assembly with 'inputFileVar' file variable nested
# - an 'OutputFile_Assembly' assembly with 'outputFileVar' file variable nested
# - 'inputFileVar' set to "InputFile.txt" contents
# - 'outputFileVar' linked to 'inputFileVar'
# When workflow is run, 'inputFileVar' passes value to 'outputFileVar'
# The temp file used to store 'outputFileVar' value is determined and copied
# to "OutputFile.txt"

import os
import shutil

import ansys.tools.variableinterop as atvi

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

# initial variables
# specify the ModelCenter workflow PXCZ path and file paths
cwd = os.getcwd()
workflow_path = os.path.join(cwd, "FileVariables.pxcz")
inputFile_path = os.path.join(cwd, "InputFile.txt")
outputFile_path = os.path.join(cwd, "OutputFile.txt")

# create input file with content and empty output file
with open(inputFile_path, "w") as ifw:
    ifw.write("inputValue = 5")

with open(outputFile_path, "w") as ofw:
    ofw.write("")

with grpcmc.Engine() as mc:
    # instantiate new Process workflow
    with mc.new_workflow(workflow_path, mcapi.WorkflowType.PROCESS) as workflow:
        print("\n- workflow created: " + workflow_path)

        # get workflow root element
        workflowRoot = workflow.get_root()

        # create assembly to contain input file variable
        inputFile_assembly = workflow.create_assembly(
            name="InputFile_Assembly",
            parent=workflowRoot,
            assembly_type=mcapi.AssemblyType.SEQUENCE,
        )
        print("- input assembly created")

        # create input file variable under assembly
        inputFile_datapin = inputFile_assembly.add_datapin("inputFileVar", atvi.VariableType.FILE)
        print("- input file variable created under input assembly")

        # get input file contents as FileValue object and set to input file variable value
        with atvi.NonManagingFileScope() as inputFile_scope:
            inputFile_contents = inputFile_scope.read_from_file(
                inputFile_path, mime_type=None, encoding=None
            )
            inputFile_datapin.set_state(atvi.VariableState(inputFile_contents, True))
            print(f"- input file variable value set to input file contents")

        # create assembly to contain output file variable
        outputFile_assembly = workflow.create_assembly(
            name="OutputFile_Assembly",
            parent=workflowRoot,
            assembly_type=mcapi.AssemblyType.SEQUENCE,
        )
        print("- output assembly created")

        # create output file variable under assembly
        outputFile_datapin = outputFile_assembly.add_datapin(
            "outputFileVar", atvi.VariableType.FILE
        )
        print("- output file variable created under output assembly")

        # don't need to set value for output file variable
        # since output file variable will get its value from link to input file variable

        # link file variables
        workflow.create_link(outputFile_datapin, inputFile_datapin)
        print(f"- workflow links created between file variables")

        # run workflow
        workflow.run(collect_names=[])
        print("\nWorkflow ran..")

        # get output file variable's temporary file path that contains updated contents after run
        # and copy to output file

        # From FileValue documentation:
        ## The FileValue instance is intended to represent an immutable value.
        ## The file returned by this call may point to a cached file or even the original file.
        ## Callers must not modify the file on disk. Otherwise, undefined behaviors,
        ## including class 3 errors, may occur. If the caller needs to modify the file,
        ## consider using the write_file method or copying the file before modifying it

        # Message from PyModelCenter SDev:
        ## You can call get_state on a file variable and what you get back should be an
        ## ansys.tools.variableinterop.FileValue or a derivative. That basically "points"
        ## to the temp file that ModelCenter is managing with the file content.
        ## You can call write_file on that to dump it out to an appropriate path.

        # outputFile_datapin.get_state().value.write_file(outputFile_path)  # gives await async error

        tempFile_path = outputFile_datapin.get_state().value.original_file_name
        shutil.copyfile(tempFile_path, outputFile_path)
        print(f"- new outputFile file variable value written to output file")

        # prompt user if workflow should be saved
        saveInput = input("\nSave workflow (y/n)? ")
        if saveInput in ["yes", "y"]:
            workflow.save_workflow()
            print("- workflow saved")
        elif saveInput in ["no", "n"]:
            print("- workflow will not be saved")
        else:
            print("Please enter 'y' or 'n'.")  # needs refactor

        # pause until user presses any key, then close workflow
        exitInput = input("\nPress any key to close the workflow and exit..")
        workflow.close_workflow()
        if saveInput in ["no", "n"]:
            os.remove(workflow_path)
