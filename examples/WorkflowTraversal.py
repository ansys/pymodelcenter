# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

import os

############################################
# Example of how to traverse the entire workflow tree
############################################
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc

cwd = os.getcwd()
workflow_filename = "TraversalExample.pxcz"
workflow_path = os.path.join(cwd, workflow_filename)

elementCache = {}


def process_element(element):
    #
    # Make sure that we only process each element once. This will
    # short-circuit a bug which causes groups to recurse infinitely.
    #
    if element.element_id in elementCache:
        return
    elementCache[element.element_id] = element
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

    print(name + " [" + element_type + "]")

    if is_control:
        print("Listing child elements...")
        elements = element.get_elements()
        for key in elements.keys():
            print(" -- [" + key + "] : Element")
            process_element(elements[key])

    print("listing " + name + " groups...")
    gr_map = element.get_groups()
    for key in gr_map.keys():
        print(" -- [" + key + "] : Group")
        process_element(gr_map[key])

    print("listing element " + name + " datapins...")
    dp_map = element.get_datapins()
    for key in dp_map.keys():
        dp_name = dp_map[key].full_name
        is_input = dp_map[key].is_input_to_component
        dp_type = dp_map[key].value_type.to_display_string()
        dp_value = dp_map[key].get_state().value
        if is_input:
            print(" ==>[" + dp_name + ":" + dp_type + "] : " + str(dp_value))
        else:
            print(" [" + dp_name + ":" + dp_type + "]==> " + str(dp_value))


print("Initializing workflow engine...")
with grpcmc.Engine() as mc:
    print("Loading workflow: " + workflow_path)
    with mc.load_workflow(workflow_path) as workflow:
        print("Loaded: " + workflow_filename)
        root = workflow.get_root()
        print("Processing root")
        process_element(root)
