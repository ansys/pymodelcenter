"""Integration tests around Component functionality"""
import os
from typing import AbstractSet, Mapping

import ansys.common.variableinterop as acvi
from ansys.engineeringworkflow.api import Property
import pytest

import ansys.modelcenter.workflow.api as mc_api
import ansys.modelcenter.workflow.grpc_modelcenter as grpcmc


def test_can_get_component_properties(workflow) -> None:
    """Verify getting component and its properties."""
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")

    # Verify actual properties.
    assert component is not None
    assert component.name == "all_types_コンポーネント"
    assert component.full_name == "ワークフロー.all_types_コンポーネント"
    assert component.element_id is not None and component.element_id
    assert component.parent_element_id is not None and component.parent_element_id
    assert component.is_connected
    assert component.pacz_url == ".\\all_types.pacz"
    assert component.control_type == "Component"
    assert component.index_in_parent == 0
    assert component.parent_assembly is not None
    assert component.groups is not None

    # Verify methods getting data.
    source: str = component.get_source()  # it's a method, should be a property?
    assert source is not None and source
    assert source == ".\\all_types.pacz"

    # Verify property names.
    property_names: AbstractSet[str] = component.get_property_names()
    assert property_names == expected_properties.keys()

    # Verify property values.
    properties: Mapping[str, Property] = component.get_properties()
    diff = {
        key: properties[key]
        for key in properties
        if key in expected_properties and properties[key].property_value != expected_properties[key]
    }
    assert len(diff) == 0

    # Verify single properties.
    for name in expected_properties.keys():
        prop: Property = component.get_property(name)
        assert prop.property_value == expected_properties[name]

    parent = component.get_parent_element()
    assert parent.name == "ワークフロー"

    position = component.get_analysis_view_position()
    assert position == (540, 128)

    # Verify variables and their types.
    variables: Mapping[str, mc_api.IDatapin] = component.get_datapins()
    diff = {
        key: variables[key]
        for key in variables
        if key in expected_variables and variables[key].value_type != expected_variables[key]
    }
    assert len(diff) == 0

    component.reconnect()


def test_handle_invoke_unknown_method(workflow) -> None:
    """Verify properly handling invoke of non-existing method."""
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")

    # Act and Verify
    # TODO: Prepare a test for invoking method.
    with pytest.raises(ValueError):
        component.invoke_method("method_yet_unknown")


def test_handle_invoke_method(engine) -> None:
    """
    Verify properly handling invoke of existing method.
    Test requires running MCRE server.
    """
    # Arrange
    workflow_name = "mcre.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), "test_files", workflow_name)
    with engine.load_workflow(file_name=workflow_path) as workflow:
        component: grpcmc.Component = workflow.get_component("Model.vehicle")
        variables: Mapping[str, mc_api.IDatapin] = component.get_datapins()
        time = variables["stopTime"]
        distance = variables["stopDistance"]

        # Run the workflow to validate outputs.
        workflow.run()

        assert time.get_value(None).is_valid
        assert distance.get_value(None).is_valid

        # Act
        component.invoke_method("Reload Input Values")

        # Verify
        assert time.get_value(None).is_valid is False
        assert distance.get_value(None).is_valid is False


def test_handle_downloading_values_from_local_component(workflow) -> None:
    """Verify properly handling downloading values from local component."""
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")

    # Act and Verify
    with pytest.raises(grpcmc.ComponentDownloadValuesFailedError):
        component.download_values()


def test_can_download_variables(engine) -> None:
    """
    Verify downloading variables from MCRE component.
    Test requires running MCRE server.
    """
    # Arrange
    workflow_name = "mcre.pxcz"
    workflow_path: str = os.path.join(os.getcwd(), "test_files", workflow_name)

    with engine.load_workflow(file_name=workflow_path) as workflow:
        component: grpcmc.Component = workflow.get_component("Model.vehicle")
        variables: Mapping[str, mc_api.IDatapin] = component.get_datapins()
        speed = variables["speed"]
        weight = variables["grossWeight"]

        speed.set_value(acvi.VariableState(value=acvi.RealValue(20.0), is_valid=True))
        weight.set_value(acvi.VariableState(value=acvi.RealValue(2750.5), is_valid=True))
        assert speed.get_value(None).value == 20.0
        assert weight.get_value(None).value == 2750.5

        # Act
        component.download_values()

        # Verify
        assert speed.get_value(None).value == 60
        assert weight.get_value(None).value == 3200


def test_invalidate_component(workflow) -> None:
    """Verify invalidate component."""
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")
    variables: Mapping[str, mc_api.IDatapin] = component.get_datapins()

    workflow.run()

    # Make sure outputs are valid.
    assert variables["boolOut"].get_value(None).is_valid
    assert variables["realOut"].get_value(None).is_valid

    component.invalidate()

    # Verify outputs are invalidated.
    assert not variables["boolOut"].get_value(None).is_valid
    assert not variables["realOut"].get_value(None).is_valid


def test_can_set_component_properties(workflow) -> None:
    """Verify setting component properties."""
    # Arrange
    component: grpcmc.Component = workflow.get_component("ワークフロー.all_types_コンポーネント")

    # Act
    component.rename("all_types_新しいコンポーネント")
    component.set_property("xposition", acvi.StringValue("600"))
    component.set_property("shouldArchive", acvi.BooleanValue(False))

    # Verify
    assert component.name == "all_types_新しいコンポーネント"
    assert component.get_property("xposition").property_value == "600"
    assert component.get_property("shouldArchive").property_value == acvi.BooleanValue(False)


expected_properties = {
    "componentRequirements": "",
    "enabled": "true",
    "custIcon": "",
    "logLevel": "20",
    "accumulatedRequirements": "",
    "author": "",
    "height": "0",
    "savedWallpaper": "",
    "xposition": "540",
    "driverAutorun": "false",
    "width": "0",
    "isDriver": False,
    "uid": "87ca469963674e0096589600",
    "allowInvalidDataAccess": "false",
    "savedIcon": "Icons/sb3kg5uof8254znz0rn6j8etdwa8qbryuia3sb3qcutadfwufas5s8ljmcvx02fhxirv4oh54\
mhgbvq7rypzpgjwkqm1n2lqph65rcx5ivfng22ixewi3m8wja8h26th.png",
    "shouldArchive": True,
    "helpURL": "",
    "onInputChange": "0",
    "inheritParentLogLevel": "true",
    "remoteNodeId": "",
    "description": "",
    "noOfThreads": "0",
    "keywords": "",
    "useDefaultQueue": "false",
    "syncInputs": "false",
    "queue": "",
    "date": "4/17/2023",
    "allowParallelRuns": "false",
    "index": "0",
    "submodel": "false",
    "icon": "",
    "driverPriority": "0",
    "runStatistics": "0.2672329,0.2660915,0.2769045,0.26851,0.2604768,0.2406731,0.2747644,\
0.1754765,0.2979679",
    "source": ".\\all_types.pacz",
    "queueList": "",
    "yposition": "128",
    "connector": "",
    "version": "",
    "bypass": False,
}

expected_variables = {
    "realIn": acvi.VariableType.REAL,
    "realOut": acvi.VariableType.REAL,
    "boolIn": acvi.VariableType.BOOLEAN,
    "intIn": acvi.VariableType.INTEGER,
    "strIn": acvi.VariableType.STRING,
    "boolOut": acvi.VariableType.BOOLEAN,
    "intOut": acvi.VariableType.INTEGER,
    "strOut": acvi.VariableType.STRING,
}
