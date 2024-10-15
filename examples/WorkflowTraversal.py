############################################
# Example of how to traverse the entire workflow tree
############################################
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
import os

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
    is_group   = isinstance(element, grpcmc.group.Group)
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
        dp_name  = dp_map[key].full_name
        is_input = dp_map[key].is_input_to_component
        dp_type  = dp_map[key].value_type.to_display_string()
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






















