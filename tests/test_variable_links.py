"""Tests for variable_links"""
import clr

clr.AddReference("phoenix-mocks/Phoenix.Mock.v45")
from Phoenix.Mock import MockVariableLink
import pytest

import ansys.modelcenter.workflow.api as mcapi


@pytest.mark.skip(reason="rewrite for grpc api")
def test_suspend_link() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)
    assert dotnet_wrapped.getCallCount("suspendLink") == 0

    # Execute
    sut.suspend_link()

    # Verify
    assert dotnet_wrapped.getCallCount("suspendLink") == 1


@pytest.mark.skip(reason="rewrite for grpc api")
def test_resume_link() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)
    assert dotnet_wrapped.getCallCount("resumeLink") == 0

    # Execute
    sut.resume_link()

    # Verify
    assert dotnet_wrapped.getCallCount("resumeLink") == 1


@pytest.mark.skip(reason="rewrite for grpc api")
def test_break_var_link() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)
    assert dotnet_wrapped.getCallCount("breakLink") == 0

    # Execute
    sut.break_link()

    # Verify
    assert dotnet_wrapped.getCallCount("breakLink") == 1


@pytest.mark.skip(reason="rewrite for grpc api")
def test_lhs_readonly() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    # The mock declares this setter public, so we should be able to do this from this angle only.
    dotnet_wrapped.LHS = "UNCHANGED"
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)

    # Execute
    with pytest.raises(AttributeError) as except_info:
        sut.lhs = "TESTFAILED"

    # Verify
    assert dotnet_wrapped.LHS == "UNCHANGED"
    assert str(except_info.value) == "can't set attribute"


@pytest.mark.skip(reason="rewrite for grpc api")
def test_read_lhs() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    dotnet_wrapped.LHS = "left hand side"
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)

    # Execute
    result: str = sut.lhs

    # Verify
    assert result == "left hand side"


@pytest.mark.skip(reason="rewrite for grpc api")
def test_write_rhs() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    dotnet_wrapped.RHS = "CHANGEME"
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)

    # Execute
    sut.rhs = "TESTPASS"

    # Verify
    assert dotnet_wrapped.RHS == "TESTPASS"


@pytest.mark.skip(reason="rewrite for grpc api")
def test_read_rhs() -> None:
    # Setup
    dotnet_wrapped: MockVariableLink = MockVariableLink()
    dotnet_wrapped.RHS = "right hand side"
    sut: mcapi.VariableLink = mcapi.VariableLink(dotnet_wrapped)

    # Execute
    result: str = sut.rhs

    # Verify
    assert result == "right hand side"
