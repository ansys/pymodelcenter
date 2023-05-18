"""Integration tests around Group functionality"""
from typing import List
import unittest

import ansys.tools.variableinterop as atvi
import pytest

import ansys.modelcenter.workflow.api as mcapi


@pytest.mark.workflow_name("linked_quadratics.pxcz")
def test_can_get_link_information(workflow) -> None:
    case = unittest.TestCase()

    # Act
    links: List[mcapi.IDatapinLink] = list(workflow.get_links())

    # Assert
    expected_rhs_to_lhs_map = {
        "Model.Quadratic.x": workflow.get_variable("Model.Quadratic1.x").element_id,
        "Model.Quadratic.a": workflow.get_variable("Model.Quadratic1.a").element_id,
        "Model.Quadratic.b": workflow.get_variable("Model.Quadratic1.b").element_id,
        "Model.Quadratic.c": workflow.get_variable("Model.Quadratic1.c").element_id,
    }
    actual_rhs_to_lhs_map = {link.rhs: link.lhs for link in links}
    case.assertCountEqual(expected_rhs_to_lhs_map, actual_rhs_to_lhs_map)


@pytest.mark.workflow_name("linked_quadratics.pxcz")
def test_can_break_a_link(workflow) -> None:
    link: mcapi.IDatapinLink = list(workflow.get_links())[0]

    # Act
    link.break_link()

    # Assert
    links = list(workflow.get_links())
    assert len(links) == 3
    assert link not in links


@pytest.mark.workflow_name("linked_quadratics.pxcz")
def test_can_suspend_and_resume_a_link(workflow) -> None:
    # Setup: Get all the links in the model as well as the link we think is involved.
    links = {link.lhs: link for link in workflow.get_links()}
    upstream_var: mcapi.IDatapin = workflow.get_variable("Model.Quadratic.x")
    downstream_var: mcapi.IDatapin = workflow.get_variable("Model.Quadratic1.x")
    control_upstream_var: mcapi.IDatapin = workflow.get_variable("Model.Quadratic.a")
    control_downstream_var: mcapi.IDatapin = workflow.get_variable("Model.Quadratic1.a")

    # Setup: Get the link we intend to suspend. Verify it looks like we think.
    assert downstream_var.element_id in links
    link = links[downstream_var.element_id]
    assert link.rhs == upstream_var.full_name

    # Setup: Get another link we don't intend to suspend. Verify it looks like we think.
    assert control_downstream_var.element_id in links
    control_link = links[control_downstream_var.element_id]
    assert control_link.rhs == control_upstream_var.full_name

    # Execute: Suspend the target link
    link.suspend()

    # Verify: Set the upstream side of the control and suspended links.
    upstream_var.set_value(atvi.VariableState(atvi.RealValue(4.7), True))
    control_upstream_var.set_value(atvi.VariableState(atvi.RealValue(867.5309), True))

    # Verify: Check that the downstream side has the value we expect.
    assert downstream_var.get_value().value == atvi.RealValue(1.0)
    assert control_downstream_var.get_value().value == atvi.RealValue(1.0)

    # Verify: Run the workflow.
    workflow.run()

    # Verify: The downstream side should not have been changed for the suspended link,
    assert downstream_var.get_value().safe_value == atvi.RealValue(1.0)
    # but it should have been for the control link.
    assert control_downstream_var.get_value().safe_value == atvi.RealValue(867.5309)

    # Execute, stage II: Resume the target link
    link.resume()

    # Verify: Set the upstream side of the control and resumed links.
    upstream_var.set_value(atvi.VariableState(atvi.RealValue(17.76), True))
    control_upstream_var.set_value(atvi.VariableState(atvi.RealValue(9000.1), True))

    # Verify: Run the workflow.
    workflow.run()

    # Verify: The downstream side should be set for both links.
    assert downstream_var.get_value().safe_value == atvi.RealValue(17.76)
    assert control_downstream_var.get_value().safe_value == atvi.RealValue(9000.1)
