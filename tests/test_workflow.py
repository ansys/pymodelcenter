"""Tests for Workflow."""
from typing import Iterable, List, Mapping, Type
import unittest

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
        if request.target.id_string == "A_COMPONENT":
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
        response = wkf_msgs.ElementInfo()
        response.id.id_string = request.name.replace(".", "_").upper()
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
        elif request.name == "model.unknown":
            response.type = elem_msgs.ELEMTYPE_VARIABLE
            response.var_type = var_msgs.VARTYPE_UNKNOWN
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

    def VariableGetState(self, request: elem_msgs.ElementIdOrName) -> var_msgs.VariableState:
        response = var_msgs.VariableState()
        if request.target_name.name == "model.boolean":
            response.value.bool_value = False
        elif request.target_name.name == "model.booleans":
            response.value.bool_array_value.values.extend([True, False, True])
        elif request.target_name.name == "model.integer":
            response.value.int_value = 42
        elif request.target_name.name == "model.integers":
            response.value.int_array_value.values.extend([86, 42, 1])
        elif request.target_name.name == "model.double":
            response.value.double_value = 3.14
        elif request.target_name.name == "model.doubles":
            response.value.double_array_value.values.extend([1.414, 0.717, 3.14])
        elif request.target_name.name == "model.string":
            response.value.string_value = "sVal"
        elif request.target_name.name == "model.strings":
            response.value.string_array_value.values.extend(["one", "two", "three"])
        elif request.target_name.name == "model.file":
            pass
        elif request.target_name.name == "model.files":
            pass
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

    def BooleanVariableSetValue(self, request):
        pass

    def IntegerVariableSetValue(self, request):
        pass

    def DoubleVariableSetValue(self, request):
        pass

    def StringVariableSetValue(self, request):
        pass

    def BooleanArraySetValue(self, request):
        pass

    def IntegerArraySetValue(self, request):
        pass

    def DoubleArraySetValue(self, request):
        pass

    def StringArraySetValue(self, request):
        pass


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
    monkeypatch_client_creation(monkeypatch, grpcmc.Assembly, mock_client)
    monkeypatch_client_creation(monkeypatch, grpcmc.Component, mock_client)
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


def test_get_component(setup_function) -> None:
    # SUT
    result: mcapi.IComponent = workflow.get_component("a.component")

    # Verification
    assert result.element_id == "A_COMPONENT"


def test_get_component_on_wrong_type(setup_function) -> None:
    # Execute
    with pytest.raises(ValueError) as err:
        result: mcapi.IComponent = workflow.get_component("a.bool")
    assert err.value.args[0] == "Element is not a component."


def test_workflow_close(setup_function) -> None:
    # Setup
    # Execute
    workflow.close_workflow()

    # Verify
    assert mock_client.was_closed


def test_workflow_auto_close(setup_function) -> None:
    # Setup
    with unittest.mock.patch.object(
        mock_client, "WorkflowClose", return_value=wkf_msgs.WorkflowCloseResponse()
    ) as mock_grpc_method:
        with grpcmc.Workflow("123", "C:\\asdf\\qwerty.pxcz") as sut:
            # SUT
            pass

        # Verification
        mock_grpc_method.assert_called_once_with(wkf_msgs.WorkflowId(id="123"))


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


set_value_tests = [
    pytest.param("BooleanVariableSetValue", acvi.BooleanValue(True), True, id="bool"),
    pytest.param("IntegerVariableSetValue", acvi.IntegerValue(42), 42, id="int"),
    pytest.param("DoubleVariableSetValue", acvi.RealValue(3.14), 3.14, id="read"),
    pytest.param("StringVariableSetValue", acvi.StringValue("strVal"), "strVal", id="str"),
    pytest.param(
        "BooleanArraySetValue",
        acvi.BooleanArrayValue(values=[True, False]),
        var_msgs.BooleanArrayValue(values=[True, False], dims=var_msgs.ArrayDimensions(dims=[2])),
        id="bool[]",
    ),
    pytest.param(
        "IntegerArraySetValue",
        acvi.IntegerArrayValue(values=[86, 42]),
        var_msgs.IntegerArrayValue(values=[86, 42], dims=var_msgs.ArrayDimensions(dims=[2])),
        id="int[]",
    ),
    pytest.param(
        "DoubleArraySetValue",
        acvi.RealArrayValue(values=[0.717, 1.414]),
        var_msgs.DoubleArrayValue(values=[0.717, 1.414], dims=var_msgs.ArrayDimensions(dims=[2])),
        id="real[]",
    ),
    pytest.param(
        "StringArraySetValue",
        acvi.StringArrayValue(values=["one", "two"]),
        var_msgs.StringArrayValue(values=["one", "two"], dims=var_msgs.ArrayDimensions(dims=[2])),
        id="str[]",
    ),
]


@pytest.mark.parametrize("request_method,src,expected", set_value_tests)
def test_set_value(setup_function, request_method: str, src: acvi.IVariableValue, expected: str):
    # Setup
    with unittest.mock.patch.object(
        mock_client,
        request_method,
        return_value=var_msgs.SetVariableValueResponse(was_changed=True),
    ) as mock_grpc_method:
        # SUT
        workflow.set_value("var.name", src)

    # Verify
    mock_grpc_method.assert_called_once()
    assert mock_grpc_method.call_args[0][0].target == elem_msgs.ElementId(id_string="VAR_NAME")
    assert mock_grpc_method.call_args[0][0].new_value == expected


get_value_tests = [
    pytest.param("model.boolean", acvi.BooleanValue(False), id="bool"),
    pytest.param("model.integer", acvi.IntegerValue(42), id="int"),
    pytest.param("model.double", acvi.RealValue(3.14), id="real"),
    pytest.param("model.string", acvi.StringValue("sVal"), id="str"),
    pytest.param(
        "model.booleans", acvi.BooleanArrayValue(values=[True, False, True]), id="bool array"
    ),
    pytest.param("model.integers", acvi.IntegerArrayValue(values=[86, 42, 1]), id="int array"),
    pytest.param(
        "model.doubles", acvi.RealArrayValue(values=[1.414, 0.717, 3.14]), id="real array"
    ),
    pytest.param(
        "model.strings", acvi.StringArrayValue(values=["one", "two", "three"]), id="str array"
    ),
]
"""Collection of tests for get_value, used in test_get_value."""


@pytest.mark.parametrize("var_name,expected", get_value_tests)
def test_get_value(setup_function, var_name: str, expected: acvi.IVariableValue):
    # SUT
    result: var_msgs.VariableState = workflow.get_value(var_name)

    # Verify
    assert result.value == expected
    assert type(result.value) == type(expected)


def test_get_value_unknown(setup_function) -> None:
    # SUT
    with pytest.raises(TypeError) as err:
        result: var_msgs.VariableState = workflow.get_value("model.unknown")

    # Verify
    assert err.value.args[0] == "Unsupported type was returned: <class 'NoneType'>"


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


@pytest.mark.parametrize("name", [pytest.param("a.assembly"), pytest.param(None)])
def test_get_assembly(setup_function, name: str):
    # SUT
    result = workflow.get_assembly(name)

    # Verify
    assert type(result) == grpcmc.Assembly


def test_get_assembly_on_wrong_type(setup_function):
    with pytest.raises(ValueError) as err:
        workflow.get_assembly("a.component")
    assert err.value.args[0] == "Element is not an assembly."


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


def test_get_variable_meta_data_on_invalid_element(setup_function) -> None:
    # SUT
    with pytest.raises(ValueError) as err:
        metadata = workflow.get_variable_meta_data("model.component")
    assert err.value.args[0] == "Element is not a variable."


def test_get_variable_meta_data_on_unknown_type(setup_function) -> None:
    # SUT
    with pytest.raises(ValueError) as err:
        metadata = workflow.get_variable_meta_data("model.unknown")
    assert err.value.args[0] == "Unknown variable type."


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


def test_halt(setup_function) -> None:
    with unittest.mock.patch.object(
        mock_client, "WorkflowHalt", return_value=wkf_msgs.WorkflowHaltResponse()
    ) as mock_grpc_method:
        # SUT
        workflow.halt()

        # Verification
        mock_grpc_method.assert_called_once_with(wkf_msgs.WorkflowHaltRequest())


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


def test_create_assembly_on_assembly(setup_function) -> None:
    # Setup
    parent = grpcmc.Assembly(element_id=elem_msgs.ElementId(id_string="Model"), channel=None)

    # Execute
    result: grpcmc.Assembly = workflow.create_assembly("newAssembly", parent)

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


def test_create_component_at_xy_pos(setup_function) -> None:
    # Setup
    response = wkf_msgs.WorkflowCreateComponentResponse()
    with unittest.mock.patch.object(
        mock_client, "WorkflowCreateComponent", return_value=response
    ) as mock_grpc_method:
        # Execute
        component: grpcmc.Component = workflow.create_component(
            server_path="common:\\Functions\\Quadratic",
            name="二次",
            parent="Model",
            init_string=None,
            av_position=(3, 5),
            insert_before=None,
        )

        # Verify
        expected_request = wkf_msgs.WorkflowCreateComponentRequest(
            source_path="common:\\Functions\\Quadratic",
            name="二次",
            init_str=None,
            parent=elem_msgs.ElementId(id_string="Model"),
            coords=elem_msgs.AnalysisViewPosition(x_pos=3, y_pos=5),
            after_comp=None,
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_create_component_after_comp_by_id(setup_function) -> None:
    # Setup
    response = wkf_msgs.WorkflowCreateComponentResponse()
    with unittest.mock.patch.object(
        mock_client, "WorkflowCreateComponent", return_value=response
    ) as mock_grpc_method:
        # Execute
        component: grpcmc.Component = workflow.create_component(
            server_path="common:\\Functions\\Quadratic",
            name="二次",
            parent="Model",
            init_string=None,
            av_position=None,
            insert_before="43q48a93cd300cab",
        )

        # Verify
        expected_request = wkf_msgs.WorkflowCreateComponentRequest(
            source_path="common:\\Functions\\Quadratic",
            name="二次",
            init_str=None,
            parent=elem_msgs.ElementId(id_string="Model"),
            coords=None,
            after_comp=elem_msgs.ElementId(id_string="43q48a93cd300cab"),
        )
        mock_grpc_method.assert_called_once_with(expected_request)


def test_create_component_after_comp_by_component(setup_function) -> None:
    # Setup
    response = wkf_msgs.WorkflowCreateComponentResponse()
    with unittest.mock.patch.object(
        mock_client, "WorkflowCreateComponent", return_value=response
    ) as mock_grpc_method:

        # Execute
        component: grpcmc.Component = workflow.create_component(
            server_path="common:\\Functions\\Quadratic",
            name="二次",
            parent="Model",
            init_string=None,
            av_position=None,
            insert_before=grpcmc.Component(
                element_id=elem_msgs.ElementId(id_string="43q48a93cd300cab"), channel=None
            ),
        )

        # Verify
        expected_request = wkf_msgs.WorkflowCreateComponentRequest(
            source_path="common:\\Functions\\Quadratic",
            name="二次",
            init_str=None,
            parent=elem_msgs.ElementId(id_string="Model"),
            coords=None,
            after_comp=elem_msgs.ElementId(id_string="43q48a93cd300cab"),
        )
        mock_grpc_method.assert_called_once_with(expected_request)


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
    validation_names = {"DESIRED_OUTPUT_VAR_1": None, "DESIRED_OUTPUT_VAR_2": None}
    collection_names = {"DESIRED_INTERMEDIATE_VAR_1": None, "DESIRED_OUTPUT_VAR_2": None}
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

    result = workflow.run(inputs, reset, validation_names, collection_names)

    expected_request = wkf_msgs.WorkflowRunRequest(
        target=wkf_msgs.WorkflowId(id="123"),
        reset=reset,
        validation_names=["DESIRED_OUTPUT_VAR_1", "DESIRED_OUTPUT_VAR_2"],
        collection_names=["DESIRED_INTERMEDIATE_VAR_1", "DESIRED_OUTPUT_VAR_2"],
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
def test_get_variable(setup_function, name: str, expected_type: Type) -> None:
    # Execute
    result: mcapi.IVariable = workflow.get_variable(name)

    # Verify
    assert type(result) == expected_type


def test_get_variable_on_wrong_type(setup_function) -> None:
    # Execute
    with pytest.raises(ValueError) as err:
        result: mcapi.IVariable = workflow.get_variable("fail")
    assert err.value.args[0] == "Element is not a variable."


@pytest.mark.parametrize(
    "name,expected_wrapper_type,expected_id",
    [
        ("a.component", mcapi.IComponent, "A_COMPONENT"),
        ("a.assembly", mcapi.IAssembly, "A_ASSEMBLY"),
        ("model.boolean", mcapi.IBooleanVariable, "MODEL_BOOLEAN"),
        ("model.integer", mcapi.IIntegerVariable, "MODEL_INTEGER"),
        ("model.string", mcapi.IStringVariable, "MODEL_STRING"),
        ("model.double", mcapi.IDoubleVariable, "MODEL_DOUBLE"),
    ],
)
def test_get_element_by_name(
    setup_function, name: str, expected_wrapper_type: Type, expected_id: str
) -> None:
    # Execute
    result: ewapi.IElement = workflow.get_element_by_name(name)

    # Verify
    assert isinstance(result, expected_wrapper_type)
    assert result.element_id == expected_id


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
