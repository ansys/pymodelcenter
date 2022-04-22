from string import Template
import win32com.client as comclient
from ansys.modelcenter.desktop.generated import modelcentertypelibrary as mclib
from ansys.engineeringworkflow.api import *
from ansys.common.variableinterop import RealValue
from concurrent.futures import *
from typing import Any
import anyio
from functools import wraps

import pythoncom


class ModelCenter(IDesktopWorkflowEngine):
    """Manages the main ModelCenter Desktop application.

    Creating an instance of this object will start an instance of ModelCenter Desktop in batch mode.
    LTTODO: add more notes on usage as the api is filled out. See the COM api documentation for
    LTTODO: some of the examples we probably want.
    """

    def __init__(self):
        self._thread = ThreadPoolExecutor(max_workers=4, initializer=lambda: pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED))
        self._instance =  None
        self._version = None
        
    # TODO: Error if not initialized from all other methods
    
    async def initialize(self) -> None:
        # TODO: Error if called twice
        def impl() -> None:
            self._instance = mclib.Application()            
            # self._instance = mclib.Application()
            # comclient.Dispatch("ModelCenter.Application") # mclib.IModelCenter(comclient.Dispatch(mclib.Application.CLSID))
            # print(self._instance)
            version = {
                "major": self._instance.version(0),
                "minor": self._instance.version(1),
                "patch": self._instance.version(2)
            }
            self._version = Template("${major}.${minor}.${patch}").safe_substitute(version)
            
        await self._to_thread(impl)

    # TODO: Do we need version property with the get_server_info call?

    @property
    def version(self) -> str:
        """
        The version of the ModelCenter Desktop application being used.
        ModelCenter versions are in the form ``1.2.3`` where

        * -1 is the major version,
        * -2 is the minor version, and
        * -3 is the patch version
        """
        return self._version

    async def _to_thread(self, func, *args, **kwargs) -> Any:
        async with anyio.from_thread.BlockingPortal() as portal:
            def _thread_impl():
                try:
                    return func(*args, **kwargs)
                finally:
                    portal.start_task_soon(portal.stop)
            future = self._thread.submit(_thread_impl)
            await portal.sleep_until_stopped()
            return future.result()

    async def get_server_info(self) -> DesktopWorkflowEngineInfo:
        def impl() -> DesktopWorkflowEngineInfo:
            # TODO: Get beta flags out?
            return DesktopWorkflowEngineInfo(self._instance.version(0), self._instance.version(1), 
                self._instance.version(2), True, "", self.version, "ModelCenter", 
                self._instance.getModelCenterPath())
        return await self._to_thread(impl)
                
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        # snot = self._instance.parallelInstance()
        # print(isinstance(snot, comclient.DispatchBaseClass))
        #test = self._instance.parallelInstance()._oleobj_.QueryInterface(mclib.IModelCenter.CLSID, pythoncom.IID_IDispatch)
        #print(test)
        #print(test.InvokeTypes(34, 0x0, 2, (3, 0), ((3, 0),),0))
        # bla = mclib.IModelCenter(snot._oleobj_)
        #print(bla)
        #print(bla._oleobj_)
        # print(bla.version(0))
        
        def impl() -> IWorkflowInstance:
            workflow_instance = mclib.IModelCenter(self._instance.parallelInstance()._oleobj_)
            workflow_instance.loadModel(file_name, mclib.constants.CONN_ERR_ERROR)
            return _WorkflowImpl(workflow_instance, self._to_thread)
        return await self._to_thread(impl)


class _WorkflowImpl(IWorkflowInstance):
    def __init__(self, workflow_instance: mclib.IModelCenter, _to_thread):
        self._instance = workflow_instance
        self._to_thread = _to_thread
        
    async def get_state(self) -> WorkflowInstanceState:
        raise NotImplementedError()

    async def run(self, inputs: Mapping[str, VariableState], reset: bool,
                  validation_ids: AbstractSet[str]) -> Mapping[str, VariableState]:
        def impl() -> Mapping[str, VariableState]:
            for var_name, var_state in inputs.items():
                self._instance.setValue(var_name, var_state.safe_value.to_api_string())
            if reset:
                # TODO: How to do this from API?
                pass
            self._instance.run(','.join(validation_ids))
            result = {}
            for var_name in validation_ids:
                var = mclib.IDoubleVariable(self._instance.getVariable(var_name)._oleobj_)
                # TODO: other types
                result[var_name] = VariableState(var.isValid(), RealValue(var.valueAbsolute))
            return result
        return await self._to_thread(impl)

    async def start_run(self, inputs: Mapping[str, VariableState], reset: bool,
                        validation_ids: AbstractSet[str]) -> str:
        raise NotImplementedError()

    # TODO: How to wait for finish in second case?

    async def get_root(self) -> IControlStatement:
        raise NotImplementedError()

    async def get_element_by_id(self, element_id: str) -> IElement:
        raise NotImplementedError()
     
