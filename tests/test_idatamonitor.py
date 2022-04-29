import ansys.common.variableinterop as acvi
import pytest

import ansys.modelcenter.workflow.api as mcapi

mock_mc: object = None
"""
Mock ModelCenter object.
Used to simulate ModelCenter's response to different API calls.
"""

workflow: mcapi.Workflow = None
"""
Workflow object under test.
"""


def setup_function(_):
    """
    Setup called before each test function in this module.
    Parameters
    ----------
    _ :
        The function about to test.
    """
    global mock_mc, workflow
    # To use when Engine supports injection of ModelCenter:
    # mock_mc = MockModelCenter()
    # engine = mcapi.Engine(mock_mc)
    engine = mcapi.Engine()
    mock_mc = engine._instance
    workflow = engine.new_workflow()


def test_get_name_of_invalid_row() -> None:
    """Testing of the get_name method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.get_name(0)

    # Verification
    assert result == ""


def test_get_name_of_valid_row() -> None:
    """Testing of the get_name method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_unlinked_item("Kraftfahrzeug-Haftpflichtversicherung")

    # SUT
    result = sut.get_name(0)

    # Verification
    assert result == "Kraftfahrzeug-Haftpflichtversicherung"


def test_set_name() -> None:
    """Testing of the set_name method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_unlinked_item("Kraftfahrzeug-Haftpflichtversicherung")

    # SUT
    sut.set_name(0, "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz")
    result = sut.get_name(0)

    # Verification
    assert result == "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz"


@pytest.mark.parametrize(
    "rename",
    [
        pytest.param(True),
        pytest.param(False),
    ]
)
def test_is_renamed(rename: bool) -> None:
    """Testing of the is_renamed method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_unlinked_item("Kraftfahrzeug-Haftpflichtversicherung")
    if rename:
        sut.set_name(0, "Rechtsschutzversicherungsgesellschaften")

    # SUT
    result = sut.is_renamed(0)

    # Verification
    assert result is rename


def test_get_link() -> None:
    """Testing of the get_link method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_item("Kraftfahrzeug-Haftpflichtversicherung",
                 "Sozialversicherungsfachangestelltenauszubildender")

    # SUT
    result = sut.get_link(0)

    # Verification
    assert result == "Sozialversicherungsfachangestelltenauszubildender"


def test_set_link() -> None:
    """Testing of the set_link method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_unlinked_item("Kraftfahrzeug-Haftpflichtversicherung")

    # SUT
    sut.set_link(0, "Betäubungsmittelverschreibungsverordnung")
    result = sut.get_link(0)

    # Verification
    assert result == "Betäubungsmittelverschreibungsverordnung"


def test_add_item() -> None:
    """Testing of the add_item method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.add_item("Massenkommunikationsdienstleistungsunternehmen",
                          "Nahrungsmittelunverträglichkeit")

    # Verification
    assert result == 0
    assert sut.get_name(0) == "Massenkommunikationsdienstleistungsunternehmen"
    assert sut.get_link(0) == "Nahrungsmittelunverträglichkeit"


def test_add_unlinked_item() -> None:
    """Testing of the add_unlinked_item method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.add_unlinked_item("Massenkommunikationsdienstleistungsunternehmen")

    # Verification
    assert result == 0
    assert sut.get_name(0) == "Massenkommunikationsdienstleistungsunternehmen"


@pytest.mark.skip(reason="Not implemented.")
def test_remove_item() -> None:
    """Testing of the remove_item method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_remove_link() -> None:
    """Testing of the remove_link method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_display_full_names() -> None:
    """Testing of the get_display_full_names method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_display_full_names() -> None:
    """Testing of the set_display_full_names method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_auto_delete() -> None:
    """Testing of the get_auto_delete method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_auto_delete() -> None:
    """Testing of the set_auto_delete method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_display_units() -> None:
    """Testing of the get_display_units method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_display_units() -> None:
    """Testing of the set_display_units method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_col_width() -> None:
    """Testing of the get_col_width method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_col_width() -> None:
    """Testing of the set_col_width method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_is_valid() -> None:
    """Testing of the is_valid method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_title() -> None:
    """Testing of the get_title method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_title() -> None:
    """Testing of the set_title method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_width() -> None:
    """Testing of the get_width method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_height() -> None:
    """Testing of the get_height method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_size() -> None:
    """Testing of the set_size method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_x() -> None:
    """Testing of the get_x method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_get_y() -> None:
    """Testing of the get_y method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def test_set_location() -> None:
    """Testing of the set_location method."""
    raise NotImplementedError
