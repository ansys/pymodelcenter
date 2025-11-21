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
"""Working with element names example for Ansys ModelCenter Workflow."""
import os

##############################################
# Working with element names (getting elements, renaming)
#
# Most elements are subclassed from AbstractRenamableElement
# Datapins and Groups are the notable exceptions
###############################################
from ansys.modelcenter.workflow.grpc_modelcenter import Engine

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
        print(
            "Do <quadratic> and <elementA> objects refer to the same element?   "
            + ("Yes!" if areSame else "No!")
        )
