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
    workflow = engine.new_workflow("workflow.pxcz")


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
    ],
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
    sut.add_item(
        "Kraftfahrzeug-Haftpflichtversicherung", "Sozialversicherungsfachangestelltenauszubildender"
    )

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
    result = sut.add_item(
        "Massenkommunikationsdienstleistungsunternehmen", "Nahrungsmittelunverträglichkeit"
    )

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


def test_remove_item() -> None:
    """Testing of the remove_item method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_unlinked_item("👀")

    # SUT
    sut.remove_item(0)

    # Verification
    assert sut.get_name(0) == ""
    # LTTODO: a real implementation should probably return None or throw


def test_remove_link() -> None:
    """Testing of the remove_link method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)
    sut.add_item("👀", "🌵")

    # SUT
    sut.remove_link(0)

    # Verification
    assert sut.get_link(0) is None


def test_get_display_full_names() -> None:
    """Testing of getting the display_full_names property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result: bool = sut.display_full_names

    # Verification
    assert result is False


def test_set_display_full_names() -> None:
    """Testing of setting the display_full_names property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.display_full_names = True
    result: bool = sut.display_full_names

    # Verification
    assert result is True


def test_get_auto_delete() -> None:
    """Testing of getting the auto_delete property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result: bool = sut.auto_delete

    # Verification
    assert result is False


def test_set_auto_delete() -> None:
    """Testing of setting the auto_delete property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.auto_delete = True
    result: bool = sut.auto_delete

    # Verification
    assert result is True


def test_get_display_units() -> None:
    """Testing of getting the display_units property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result: bool = sut.display_units

    # Verification
    assert result is False


def test_set_display_units() -> None:
    """Testing of setting the display_units property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.display_units = True
    result: bool = sut.display_units

    # Verification
    assert result is True


def test_get_col_width() -> None:
    """Testing of the get_col_width method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.get_col_width(0)

    # Verification
    assert result == 10


def test_set_col_width() -> None:
    """Testing of the set_col_width method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.set_col_width(0, 5)
    result = sut.get_col_width(0)

    # Verification
    assert result == 5


def test_is_valid() -> None:
    """Testing of the is_valid method."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.is_valid()

    # Verification
    assert result is True


def test_get_title() -> None:
    """Testing of getting the title property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.title

    # Verification
    assert result == "a"


def test_set_title() -> None:
    """Testing of setting the title property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.title = "☕"
    result = sut.title

    # Verification
    assert result == "☕"


def test_get_size() -> None:
    """Testing of getting the size property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    result = sut.size

    # Verification
    assert result == (100, 50)


def test_set_size() -> None:
    """Testing of setting the size property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.size = (50, 100)
    result = sut.size

    # Verification
    assert result == (50, 100)


def test_get_location() -> None:
    """Testing of getting the location property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 10, 20)

    # SUT
    result = sut.location

    # Verification
    assert result == (10, 20)


def test_set_location() -> None:
    """Testing of setting the location property."""
    # Setup
    sut: mcapi.DataMonitor = workflow.create_data_monitor("comp", "a", 0, 0)

    # SUT
    sut.location = (10, 20)
    result = sut.location

    # Verification
    assert result == (10, 20)
