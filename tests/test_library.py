import pytest
import ansys.modelcenter.workflow.api as mcapi


def test_placeholder():
    engine = mcapi.engine.Engine()
    engine.new_workflow(mcapi.WorkflowType.PROCESS)
    assert True
