"""Integration tests around Group functionality"""
from typing import List
import unittest

import pytest

import ansys.modelcenter.workflow.api as mcapi


@pytest.mark.workflow_name("linked_quadratics.pxcz")
def test_can_get_link_information(workflow) -> None:
    case = unittest.TestCase()

    # Act
    links: List[mcapi.IVariableLink] = list(workflow.get_links())

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
    link: mcapi.IVariableLink = list(workflow.get_links())[0]

    # Act
    link.break_link()

    # Assert
    links = list(workflow.get_links())
    assert len(links) == 3
    assert link not in links
