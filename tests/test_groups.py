import pytest


@pytest.mark.skip(reason="Not implemented.")
def count():
    """Testing of the count method."""
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented.")
def item(id_) -> object:
    """Testing of the item method."""
    raise NotImplementedError
