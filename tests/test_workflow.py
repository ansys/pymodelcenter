"""Tests for Workflow."""
from typing import Iterable, List, Mapping, Type

import ansys.common.variableinterop as acvi
import ansys.engineeringworkflow.api as ewapi
import pytest

import ansys.modelcenter.workflow.api as mcapi
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc
import ansys.modelcenter.workflow.grpc_modelcenter.proto.element_messages_pb2 as elem_msgs  # noqa: 501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.variable_value_messages_pb2 as var_msgs  # noqa: 501
import ansys.modelcenter.workflow.grpc_modelcenter.proto.workflow_messages_pb2 as wkf_msgs  # noqa: 501

from .grpc_server_test_utils.client_creation_monkeypatch import monkeypatch_client_creation


class MockWorkflowClientForWorkflowTest:
    def __init__(self) -> None:
        self.was_saved: bool = False
        self.was_save_asd: bool = False
        self.was_closed: bool = False
        self.was_component_removed: bool = False
        self.was_link_created: bool = False
        self.workflow_run_requests: List[wkf_msgs.WorkflowRunRequest] = []
        self.workflow_run_response = wkf_msgs.WorkflowRunResponse()

    def AssemblyAddAssembly(
        self, request: elem_msgs.AddAssemblyRequest
    ) -> elem_msgs.AddAssemblyResponse:
        el_id = elem_msgs.ElementId(id_string=request.parent.id_string + "." + request.name.name)
        response = elem_msgs.AddAssemblyResponse(id=el_id)
        return response

    def WorkflowGetRoot(self, request: wkf_msgs.WorkflowId) -> wkf_msgs.WorkflowGetRootResponse:
        response = wkf_msgs.WorkflowGetRootResponse()
        response.id.id_string = "Model"
        return response

    def WorkflowGetDirectory(
        self, request: wkf_msgs.WorkflowId
    ) -> wkf_msgs.WorkflowGetDirectoryResponse:
        response = wkf_msgs.WorkflowGetDirectoryResponse()
        if request.id == "123":
            response.workflow_dir = "D:\\Some\\Path"
        return response

    def WorkflowSave(self, request: wkf_msgs.WorkflowId) -> wkf_msgs.WorkflowSaveResponse:
        if request.id == "123":
            self.was_saved = True
        response = wkf_msgs.WorkflowSaveResponse()
        return response

    def WorkflowSaveAs(
        self, request: wkf_msgs.WorkflowSaveAsRequest
    ) -> wkf_msgs.WorkflowSaveResponse:
        if request.target.id == "123" and request.new_target_path == "jkl;":
            self.was_save_asd = True
        response = wkf_msgs.WorkflowSaveResponse()
        return response

    def WorkflowClose(self, request: wkf_msgs.WorkflowId) -> wkf_msgs.WorkflowCloseResponse:
        if request.id == "123":
            self.was_closed = True
        response = wkf_msgs.WorkflowCloseResponse()
        return response

    def WorkflowRemoveComponent(self, request: wkf_msgs.WorkflowRemoveComponentRequest):
        response = wkf_msgs.WorkflowRemoveComponentResponse()
        if request.target.id_string == "3457134":
            response.existed = True
            self.was_component_removed = True
        return response

    def WorkflowCreateComponent(self, request: wkf_msgs.WorkflowCreateComponentRequest):
        response = wkf_msgs.WorkflowCreateComponentResponse()
        response.created.id_string = "zxcv"
        return response

    def WorkflowCreateLink(self, request: wkf_msgs.WorkflowCreateLinkRequest):
        if request.target.id_string != "inputs.var1" or request.equation != "Workflow.comp.output4":
            raise Exception()
        self.was_link_created = True
        response = wkf_msgs.WorkflowCreateLinkResponse()
        return response

    def WorkflowAutoLink(self, request: wkf_msgs.WorkflowAutoLinkRequest):
        response = wkf_msgs.WorkflowAutoLinkResponse()
        if (
            request.source_comp.id_string == "Workflow.source_comp"
            and request.target_comp.id_string == "Workflow.dest_comp"
        ):
            link = response.created_links.add()
            link.lhs.id_string = "a"
            link.rhs = "1"
            link = response.created_links.add()
            link.lhs.id_string = "b"
            link.rhs = "2"
        return response

    def WorkflowGetLinksRequest(self, request: wkf_msgs.WorkflowId):
        response = wkf_msgs.WorkflowGetLinksResponse()
        if request.id == "12345":
            link = response.links.add()
            link.lhs.id_string = "linkTarget1"
            link.rhs = "a"
            link = response.links.add()
            link.lhs.id_string = "linkTarget2"
            link.rhs = "b"
            link = response.links.add()
            link.lhs.id_string = "linkTarget3"
            link.rhs = "c"
        return response

    def WorkflowBreakLink(self, request: wkf_msgs.WorkflowBreakLinkRequest):
        response = wkf_msgs.WorkflowBreakLinkResponse()
        if request.target_var.id_string == "jkl;":
            response.existed = True
        return response

    def WorkflowGetElementByName(self, request: elem_msgs.ElementName):
        response = wkf_msgs.WorkflowGetElementByNameResponse()
        response.id.id_string = request.name
        if request.name == "a.component":
            response.type = elem_msgs.ELEMTYPE_COMPONENT
        elif request.name == "a.assembly":
            response.type = elem_msgs.ELEMTYPE_ASSEMBLY
        elif request.name == "model.boolean":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_BOOLEAN
        elif request.name == "model.booleans":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_BOOLEAN_ARRAY
        elif request.name == "model.double":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_REAL
        elif request.name == "model.doubles":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_REAL_ARRAY
        elif request.name == "model.integer":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_INTEGER
        elif request.name == "model.integers":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_INTEGER_ARRAY
        elif request.name == "model.string":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_STRING
        elif request.name == "model.strings":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_STRING_ARRAY
        return response

    def WorkflowHalt(self, request: wkf_msgs.WorkflowHaltRequest):
        response = wkf_msgs.WorkflowHaltResponse()
        return response

    def VariableGetType(self, request: elem_msgs.ElementId):
        response = var_msgs.VariableTypeResponse()
        if request.id_string == "model.boolean":
            response.var_type = var_msgs.VARTYPE_BOOLEAN
        elif request.id_string == "model.booleans":
            response.var_type = var_msgs.VARTYPE_BOOLEAN_ARRAY
        elif request.id_string == "model.integer":
            response.var_type = var_msgs.VARTYPE_INTEGER
        elif request.id_string == "model.integers":
            response.var_type = var_msgs.VARTYPE_INTEGER_ARRAY
        elif request.id_string == "model.double":
            response.var_type = var_msgs.VARTYPE_REAL
        elif request.id_string == "model.doubles":
            response.var_type = var_msgs.VARTYPE_REAL_ARRAY
        elif request.id_string == "model.string":
            response.var_type = var_msgs.VARTYPE_STRING
        elif request.id_string == "model.strings":
            response.var_type = var_msgs.VARTYPE_STRING_ARRAY
        elif request.id_string == "model.file":
            response.var_type = var_msgs.VARTYPE_FILE
        elif request.id_string == "model.files":
            response.var_type = var_msgs.VARTYPE_FILE_ARRAY
        return response

    def BooleanVariableGetMetadata(self, request: elem_msgs.ElementId):
        response = var_msgs.BooleanVariableMetadata()
        response.base_metadata.description = "☯"
        return response

    def DoubleVariableGetMetadata(self, request: elem_msgs.ElementId):
        response = var_msgs.DoubleVariableMetadata()
        response.base_metadata.description = "☯"
        response.numeric_metadata.units = "§"
        response.numeric_metadata.display_format = "※"
        response.lower_bound = 1.1
        response.upper_bound = 4.4
        response.enum_values.extend([1.1, 2.2, 3.3, 4.4])
        response.enum_aliases.extend(["a", "b", "c", "d"])
        return response

    def IntegerVariableGetMetadata(self, request: elem_msgs.ElementId):
        response = var_msgs.IntegerVariableMetadata()
        response.base_metadata.description = "☯"
        response.numeric_metadata.units = "§"
        response.numeric_metadata.display_format = "※"
        response.lower_bound = 1
        response.upper_bound = 4
        response.enum_values.extend([1, 2, 3, 4])
        response.enum_aliases.extend(["a", "b", "c", "d"])
        return response

    def StringVariableGetMetadata(self, request: elem_msgs.ElementId):
        response = var_msgs.StringVariableMetadata()
        response.base_metadata.description = "☯"
        response.enum_values.extend(["1", "2", "3", "4"])
        response.enum_aliases.extend(["a", "b", "c", "d"])
        return response

    def FileVariableGetMetadata(self, request: elem_msgs.ElementId):
        response = var_msgs.FileVariableMetadata()
        response.base_metadata.description = "☯"
        return response

    def WorkflowRun(self, request: wkf_msgs.WorkflowRunRequest) -> wkf_msgs.WorkflowRunResponse:
        self.workflow_run_requests.append(request)
        return self.workflow_run_response

    def ElementGetFullName(self, request: elem_msgs.ElementId) -> elem_msgs.ElementName:
        return elem_msgs.ElementName(name=request.id_string)


mock_client: MockWorkflowClientForWorkflowTest

workflow: grpcmc.Workflow
"""
Workflow object under test.
"""


@pytest.fixture
def setup_function(monkeypatch):
    """
    Setup called before each test function in this module.
    """

    global mock_client
    mock_client = MockWorkflowClientForWorkflowTest()
    monkeypatch_client_creation(monkeypatch, grpcmc.Workflow, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.BooleanVariable, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.BooleanArray, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.DoubleVariable, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.DoubleArray, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.IntegerVariable, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.IntegerArray, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.StringVariable, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.StringArray, mock_client)

    global workflow
    workflow = grpcmc.Workflow("123", "C:\\asdf\\qwerty.pxcz")


def test_get_root(setup_function) -> None:
    # SUT
    result: ewapi.IControlStatement = workflow.get_root()

    # Verification
    assert result.element_id == "Model"


# def test_get_element_by_id(setup_function):
#     pass


def test_get_component(setup_function) -> None:
    # SUT
    result: mcapi.IComponent = workflow.get_component("a.component")

    # Verification
    assert result.element_id == "a.component"


def test_workflow_close(setup_function) -> None:
    # Setup
    # Execute
    workflow.close_workflow()

    # Verify
    assert mock_client.was_closed


def test_workflow_directory(setup_function) -> None:
    """
    Testing of workflow_directory method.
    """
    # SUT
    result = workflow.workflow_directory

    # Verify
    assert isinstance(result, str)
    assert result == "D:\\Some\\Path"


def test_workflow_file_name(setup_function):
    """
    Testing of workflow_file_name method.
    """
    # SUT
    result = workflow.workflow_file_name

    # Verify
    assert isinstance(result, str)
    assert result == "qwerty.pxcz"


# set_value_tests = [
#     pytest.param(acvi.BooleanValue(True), "True", id="bool"),
#     pytest.param(acvi.IntegerValue(42), "42", id="int"),
#     pytest.param(acvi.RealValue(3.14), "3.14", id="read"),
#     pytest.param(acvi.StringValue("strVal"), "strVal", id="str"),
#     pytest.param(acvi.BooleanArrayValue(values=[True, False]), "True,False", id="bool[]"),
#     pytest.param(acvi.IntegerArrayValue(values=[86, 42]), "86,42", id="int[]"),
#     pytest.param(acvi.RealArrayValue(values=[0.717, 1.414]), "0.717,1.414", id="real[]"),
#     pytest.param(acvi.StringArrayValue(values=["one", "two"]), '"one","two"', id="str[]"),
#     pytest.param("Some String", "Some String", id="raw str"),
#     pytest.param(14.44, "14.44", id="raw float"),
# ]
#
#
# @pytest.mark.parametrize("src,expected", set_value_tests)
# def test_set_value(src: Any, expected: str):
#     """
#     Testing of set_value method.
#     """
#     global mock_mc, workflow
#
#     # SUT
#     workflow.set_value("var.name", src)
#
#     # Verify
#     assert mock_mc.getCallCount("setValue") == 1
#     args = mock_mc.getLastArgumentRecord("setValue")
#     assert args[0] == "var.name"
#     result = args[1]
#     assert type(result) == str
#     assert result == expected
#
#
# get_value_tests = [
#     pytest.param("root.b", acvi.BooleanValue(False), id="bool"),
#     pytest.param("root.i", acvi.IntegerValue(42), id="int"),
#     pytest.param("root.r", acvi.RealValue(3.14), id="real"),
#     pytest.param("root.s", acvi.StringValue("sVal"), id="str"),
#     pytest.param("root.b_a", acvi.BooleanArrayValue(values=[True, False, True]), id="bool array"),
#     pytest.param("root.i_a", acvi.IntegerArrayValue(values=[86, 42, 1]), id="int array"),
#     pytest.param("root.r_a", acvi.RealArrayValue(values=[1.414, 0.717, 3.14]), id="real array"),
#   pytest.param("root.s_a", acvi.StringArrayValue(values=["one", "two", "three"]), id="str array"),
# ]
# """Collection of tests for get_value, used in test_get_value."""
#
#
# def setup_test_values():
#     """
#     Setup some values usable of testing get_value and \
#     get_value_absolute.
#     """
#     global mock_mc
#     mock_mc.createAssemblyVariable("b", "Input", "root")
#     mock_mc.createAssemblyVariable("i", "Input", "root")
#     mock_mc.createAssemblyVariable("r", "Input", "root")
#     mock_mc.createAssemblyVariable("s", "Input", "root")
#     mock_mc.createAssemblyVariable("b_a", "Input", "root")
#     mock_mc.createAssemblyVariable("i_a", "Input", "root")
#     mock_mc.createAssemblyVariable("r_a", "Input", "root")
#     mock_mc.createAssemblyVariable("s_a", "Input", "root")
#     vars_ = py_list_to_net_typed_list(
#         ["root.b", "root.i", "root.r", "root.s", "root.b_a", "root.i_a", "root.r_a", "root.s_a"]
#     )
#     vals = py_list_to_net_list(
#         [
#             False,
#             42,
#             3.14,
#             "sVal",
#             [True, False, True],
#             [86, 42, 1],
#             [1.414, 0.717, 3.14],
#             ["one", "two", "three"],
#         ]
#     )
#     mock_mc.SetMockValues(vars_, vals)
#
#
# @pytest.mark.parametrize("var_name,expected", get_value_tests)
# def test_get_value(var_name: str, expected: acvi.IVariableValue):
#     """
#     Testing of get_value_tests method pulling each of the different
#     variable types.
#     """
#     global mock_mc, workflow
#     setup_test_values()
#
#     # SUT
#     result = workflow.get_value(var_name)
#
#     # Verify
#     assert result == expected
#     assert type(result) == type(expected)
#     assert mock_mc.getCallCount("getValue")
#
#
# value_absolute_tests = get_value_tests.copy()
# """Collection of test for get_value_absolute.
#
# Reusing the tests for get_values, but then adding some additional tests
# below."""
#
# value_absolute_tests.extend(
#     [
#         pytest.param("root.b_a[1]", acvi.BooleanValue(False), id="bool array indexed"),
#         pytest.param("root.i_a[2]", acvi.IntegerValue(1), id="int array indexed"),
#         pytest.param("root.r_a[0]", acvi.RealValue(1.414), id="real array indexed"),
#         pytest.param("root.s_a[1]", acvi.StringValue("two"), id="str array indexed"),
#     ]
# )
#
#
# @pytest.mark.parametrize("var_name,expected", value_absolute_tests)
# def test_get_value_absolute(var_name: str, expected: acvi.IVariableValue):
#     """
#     Testing of get_value_tests method pulling each of the different \
#     variable types.
#     """
#     global mock_mc, workflow
#     setup_test_values()
#
#     # SUT
#     result = workflow.get_value_absolute(var_name)
#
#     # Verify
#     assert result == expected
#     assert type(result) == type(expected)
#     assert mock_mc.getCallCount("getValueAbsolute")
#
#
# @pytest.mark.parametrize("schedular", ["forward", "backward", "mixed", "script"])
# def test_set_scheduler(schedular: str) -> None:
#     """
#     Testing of set_scheduler method with different schedular values
#     Parameters
#     ----------
#     schedular :  str
#         schedular value to test
#     """
#     global mock_mc, workflow
#
#     # SUT
#     workflow.set_scheduler(schedular)
#
#     # Verify
#     assert mock_mc.getCallCount("setScheduler") == 1
#     args: list = mock_mc.getLastArgumentRecord("setScheduler")
#     assert len(args) == 1
#     assert args[0] == schedular


def test_remove_component(setup_function):
    """Testing of remove_component method."""
    # SUT
    workflow.remove_component("a.component")

    # Verify
    assert mock_client.was_component_removed


def test_get_assembly(setup_function):
    # SUT
    result = workflow.get_assembly("a.assembly")

    # Verify
    assert type(result) == grpcmc.Assembly


@pytest.mark.parametrize("is_array", [pytest.param(True), pytest.param(False)])
def test_get_bool_meta_data(setup_function, is_array: bool) -> None:
    # Setup
    var = "model.booleans" if is_array else "model.boolean"
    expected_type = acvi.VariableType.BOOLEAN_ARRAY if is_array else acvi.VariableType.BOOLEAN

    # SUT
    metadata = workflow.get_variable_meta_data(var)

    # Verification
    assert metadata.variable_type == expected_type
    assert metadata.description == "☯"


@pytest.mark.parametrize("is_array", [pytest.param(True), pytest.param(False)])
def test_get_int_meta_data(setup_function, is_array: bool) -> None:
    # Setup
    var = "model.integers" if is_array else "model.integer"
    expected_type = acvi.VariableType.INTEGER_ARRAY if is_array else acvi.VariableType.INTEGER

    # SUT
    metadata = workflow.get_variable_meta_data(var)

    # Verification
    assert metadata.variable_type == expected_type
    assert metadata.description == "☯"
    assert metadata.units == "§"
    assert metadata.display_format == "※"
    assert metadata.lower_bound == 1
    assert metadata.upper_bound == 4
    assert metadata.enumerated_values == [1, 2, 3, 4]
    assert metadata.enumerated_aliases == ["a", "b", "c", "d"]


@pytest.mark.parametrize("is_array", [pytest.param(True), pytest.param(False)])
def test_get_real_meta_data(setup_function, is_array: bool) -> None:
    # Setup
    var = "model.doubles" if is_array else "model.double"
    expected_type = acvi.VariableType.REAL_ARRAY if is_array else acvi.VariableType.REAL

    # SUT
    metadata = workflow.get_variable_meta_data(var)

    # Verification
    assert metadata.variable_type == expected_type
    assert metadata.description == "☯"
    assert metadata.units == "§"
    assert metadata.display_format == "※"
    assert metadata.lower_bound == 1.1
    assert metadata.upper_bound == 4.4
    assert metadata.enumerated_values == [1.1, 2.2, 3.3, 4.4]
    assert metadata.enumerated_aliases == ["a", "b", "c", "d"]


@pytest.mark.parametrize("is_array", [pytest.param(True), pytest.param(False)])
def test_get_string_meta_data(setup_function, is_array: bool) -> None:
    # Setup
    var = "model.strings" if is_array else "model.string"
    expected_type = acvi.VariableType.STRING_ARRAY if is_array else acvi.VariableType.STRING

    # SUT
    metadata = workflow.get_variable_meta_data(var)

    # Verification
    assert metadata.variable_type == expected_type
    assert metadata.description == "☯"
    assert metadata.enumerated_values == ["1", "2", "3", "4"]
    assert metadata.enumerated_aliases == ["a", "b", "c", "d"]


@pytest.mark.parametrize("is_array", [pytest.param(True), pytest.param(False)])
@pytest.mark.skip("Re-enable when file support added to WorkflowGetElementByNameResponse")
def test_get_file_meta_data(setup_function, is_array: bool) -> None:
    # Setup
    var = "model.files" if is_array else "model.file"
    expected_type = acvi.VariableType.FILE_ARRAY if is_array else acvi.VariableType.FILE

    # SUT
    metadata = workflow.get_variable_meta_data(var)

    # Verification
    assert metadata.variable_type == expected_type
    assert metadata.description == "☯"


@pytest.mark.parametrize(
    "workflow_id,link_lhs_values",
    [
        pytest.param("54321", [], id="empty"),
        pytest.param("12345", ["linkTarget1", "linkTarget2", "linkTarget3"], id="some links"),
    ],
)
def test_get_links(setup_function, workflow_id: str, link_lhs_values: Iterable[str]) -> None:
    """
    Verify that get_links works when there are no links.
    """
    # Setup
    workflow._id = workflow_id

    # Execute
    links: Iterable[mcapi.IVariableLink] = workflow.get_links()

    # Verify
    assert [link.lhs for link in links] == link_lhs_values


def test_get_uuid(setup_function) -> None:
    # Execute
    result: str = workflow.get_workflow_uuid()

    # Verify
    assert result == "123"


def test_auto_link(setup_function) -> None:
    # Execute
    links: List[mcapi.IVariableLink] = workflow.auto_link(
        "Workflow.source_comp", "Workflow.dest_comp"
    )

    # Verify
    assert len(links) == 2
    assert links[0].lhs == "a"
    assert links[0].rhs == "1"
    assert links[1].lhs == "b"
    assert links[1].rhs == "2"


def test_create_assembly(setup_function) -> None:
    # Execute
    result: grpcmc.Assembly = workflow.create_assembly("newAssembly", "Model")

    # Verify
    assert result.element_id == "Model.newAssembly"


def test_save_workflow(setup_function):
    # Execute
    workflow.save_workflow()

    # Verify
    assert mock_client.was_saved


def test_save_workflow_as(setup_function):
    # Execute
    workflow.save_workflow_as("jkl;")

    # Verify
    assert mock_client.was_save_asd


def test_create_component(setup_function) -> None:
    # Execute
    component: grpcmc.Component = workflow.create_component(
        server_path="common:\\Functions\\Quadratic",
        name="二次",
        parent="Model",
        init_string=None,
        av_position=None,
        insert_before=None,
    )

    # Verify
    assert component.element_id == "zxcv"


def test_create_link(setup_function) -> None:
    test_var_name = "inputs.var1"
    test_eqn = "Workflow.comp.output4"

    # Execute
    workflow.create_link(test_var_name, test_eqn)

    # Verify
    assert mock_client.was_link_created is True


def test_create_link_with_objects(setup_function) -> None:
    lhs = elem_msgs.ElementId(id_string="inputs.var1")
    test_var = grpcmc.DoubleVariable(lhs, workflow._channel)
    rhs = elem_msgs.ElementId(id_string="Workflow.comp.output4")
    test_eqn_var = grpcmc.DoubleVariable(rhs, workflow._channel)

    # Execute
    workflow.create_link(test_var, test_eqn_var)

    # Verify
    assert mock_client.was_link_created is True


@pytest.mark.parametrize("reset", [True, False])
def test_run_synchronous(setup_function, reset: bool) -> None:
    # Using a dict as an ordered set
    validation_ids = {"DESIRED_OUTPUT_VAR_1": None, "DESIRED_OUTPUT_VAR_2": None}
    inputs: Mapping[str, acvi.VariableState] = {
        "INPUT_VAR_1": acvi.VariableState(is_valid=True, value=acvi.IntegerValue(47)),
        "INPUT_VAR_2": acvi.VariableState(is_valid=False, value=acvi.RealValue(-867.5309)),
        "INPUT_VAR_3": acvi.VariableState(is_valid=True, value=acvi.BooleanValue(True)),
        "INPUT_VAR_4": acvi.VariableState(
            is_valid=True, value=acvi.StringValue("this is a test string")
        ),
    }

    mock_response = wkf_msgs.WorkflowRunResponse()
    mock_response.results["DESIRED_OUTPUT_VAR_1"].is_valid = False
    mock_response.results["DESIRED_OUTPUT_VAR_1"].value.MergeFrom(
        var_msgs.VariableValue(double_value=9000.1)
    )
    mock_response.results["DESIRED_OUTPUT_VAR_2"].is_valid = True
    mock_response.results["DESIRED_OUTPUT_VAR_1"].value.MergeFrom(
        var_msgs.VariableValue(int_value=4858)
    )
    mock_client.workflow_run_response = wkf_msgs.WorkflowRunResponse()

    result = workflow.run(inputs, reset, validation_ids)

    expected_request = wkf_msgs.WorkflowRunRequest(
        target=wkf_msgs.WorkflowId(id="123"),
        reset=reset,
        validation_ids=["DESIRED_OUTPUT_VAR_1", "DESIRED_OUTPUT_VAR_2"],
        inputs={
            "INPUT_VAR_1": var_msgs.VariableState(
                is_valid=True, value=var_msgs.VariableValue(int_value=47)
            ),
            "INPUT_VAR_2": var_msgs.VariableState(
                is_valid=False, value=var_msgs.VariableValue(double_value=-867.5309)
            ),
            "INPUT_VAR_3": var_msgs.VariableState(
                is_valid=True, value=var_msgs.VariableValue(bool_value=True)
            ),
            "INPUT_VAR_4": var_msgs.VariableState(
                is_valid=True, value=var_msgs.VariableValue(string_value="this is a test string")
            ),
        },
    )
    assert mock_client.workflow_run_requests == [expected_request]


@pytest.mark.parametrize(
    "name,expected_type",
    [
        pytest.param("model.boolean", grpcmc.BooleanVariable),
        pytest.param("model.booleans", grpcmc.BooleanArray),
        pytest.param("model.double", grpcmc.DoubleVariable),
        pytest.param("model.doubles", grpcmc.DoubleArray),
        pytest.param("model.integer", grpcmc.IntegerVariable),
        pytest.param("model.integers", grpcmc.IntegerArray),
        pytest.param("model.string", grpcmc.StringVariable),
        pytest.param("model.strings", grpcmc.StringArray),
    ],
)
@pytest.mark.skip("Re-enable when create_variable is implemented")
def test_get_variable(setup_function, name: str, expected_type: Type) -> None:
    # Execute
    result: mcapi.IVariable = workflow.get_variable(name)

    # Verify
    assert type(result) == expected_type


# @pytest.mark.parametrize(
#     "variables",
#     [
#         pytest.param(None),
#         pytest.param("Model.a,Model.b,Model.c"),
#     ],
# )
# def test_run(variables: Optional[str]) -> None:
#     # Setup
#     global workflow
#
#     # SUT
#     workflow.run_variables(variables)
#
#     # Verification
#     assert workflow._instance.getCallCount("run") == 1
#     expected_arg: str = variables or ""
#     assert workflow._instance.getArgumentRecord("run", 0) == [expected_arg]
#
#
# @pytest.mark.parametrize(
#     "index",
#     [
#         pytest.param(0),
#         pytest.param(2),
#     ],
# )
# def test_get_datamonitor(index: int) -> None:
#     # Setup
#     global workflow
#     for x in range(index + 1):
#         workflow.create_data_monitor("comp", "DM" + str(x), 0, 0)
#
#     # SUT
#     result: mcapi.IDataMonitor = workflow.get_data_monitor("comp", index)
#
#     # Verification
#     assert result.title == "DM" + str(index)
#
#
# def test_create_datamonitor() -> None:
#     # Setup
#     global workflow
#
#     # SUT
#     result: mcapi.IDataMonitor = workflow.create_data_monitor("comp", "DM0", 0, 0)
#
#     # Verification
#     assert result.title == "DM0"
#
#
# def test_remove_datamonitor() -> None:
#     # Setup
#     global workflow
#     workflow.create_data_monitor("comp", "DM0", 0, 0)
#
#     # SUT
#     result: bool = workflow.remove_data_monitor("comp", 0)
#
#     # Verification
#     assert result is True
#
#
# def test_remove_datamonitor_at_invalid_index() -> None:
#     # Setup
#     global workflow
#
#     # SUT
#     result: bool = workflow.remove_data_monitor("comp", 0)
#
#     # Verification
#     assert result is False
#
#
