import ansys.modelcenter.workflow.api as mcapi


####################################################################################################
# Setup for every test
####################################################################################################
sut: mcapi.IRefArrayProp


def setup_function():
    """Setup called before each test in this module."""
    global sut
    sut = mcapi.IRefArrayProp('test name', 'test type')

    sut.enum_values = 'test enumerated values'
    sut.is_input = True
    sut.title = 'test title'
    sut.description = 'test description'

####################################################################################################


def test_enum_values() -> None:
    """Testing of the enum_values property."""
    # SUT
    original_enum_values = sut.enum_values
    sut.enum_values = 'new enumerated values'

    # Verify
    assert original_enum_values == 'test enumerated values'
    assert sut.enum_values == 'new enumerated values'


def test_is_input() -> None:
    """Testing of the is_input property."""
    # SUT
    original_is_input = sut.is_input
    sut.is_input = False

    # verify
    assert original_is_input
    assert not sut.is_input


def test_title() -> None:
    """Testing of the title property."""
    # SUT
    original_title = sut.title
    sut.title = 'new title'

    # Verify
    assert original_title == 'test title'
    assert sut.title == 'new title'


def test_description() -> None:
    """Testing of the description property."""
    # SUT
    original_description = sut.description
    sut.description = 'new description'

    # Verify
    assert original_description == 'test description'
    assert sut.description == 'new description'


def test_get_name() -> None:
    """Testing of the get_name method."""
    # SUT
    result = sut.get_name()

    # Verify
    assert result == 'test name'


def test_get_type() -> None:
    """Testing of the get_type method."""
    # SUT
    result = sut.get_type()

    # Verify
    assert result == 'test type'
