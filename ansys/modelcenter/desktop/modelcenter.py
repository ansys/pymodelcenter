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
        # Use a ThreadPoolExecutor to proxy all COM calls onto safe threads so that blocking com calls don't mess up our async/await-ness
        # Technically max_workers could be 1, but in reality someone will probably want to load multiple workflows at once?
        self._thread = ThreadPoolExecutor(max_workers=4, initializer=lambda: pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED))
        self._instance =  None
        
    # TODO: Error if not initialized from all other methods
    
    async def initialize(self) -> None:
        # TODO: Error if called twice
        def impl() -> None:
            self._instance = mclib.Application()            
            
            # Other ways to instantiate MC that didn't quite work right. The above gives you a proper typed object.
            # NOTE that pythoncom will fall-back on late-binding if you aren't super careful and the call semantics 
            # for some properties is different between late and eary binding.
            # comclient.Dispatch("ModelCenter.Application") 
            # mclib.IModelCenter(comclient.Dispatch(mclib.Application.CLSID))
            # print(self._instance)
            
        await self._to_thread(impl)

    async def _to_thread(self, func, *args, **kwargs) -> Any:
        """Helper that proxies all calls to a multi-threaded worker thread with anyio async on this side"""
        # Create a blocking portal so we can signal back to our thread
        async with anyio.from_thread.BlockingPortal() as portal:
            future = self._thread.submit(func, *args, **kwargs)
            # portal.stop() is an async method. It isn't documented whether it is safe to call it
            # from other threads, but since those other threads aren't the async/await thread, you'll
            # get a warning if you do call it from elsewhere. So proxy the call back to us.
            future.add_done_callback(lambda f: portal.start_task_soon(portal.stop))
            await portal.sleep_until_stopped()
            return future.result()

    async def get_server_info(self) -> DesktopWorkflowEngineInfo:
        def impl() -> DesktopWorkflowEngineInfo:
            # TODO: Get beta flags out
            maj = self._instance.version(0)
            min = self._instance.version(1)
            patch = self._instance.version(2)
            return DesktopWorkflowEngineInfo(maj, min, 
                patch, True, "", 
                f"{maj}.{min}.{patch}", "ModelCenter", 
                self._instance.getModelCenterPath())
        return await self._to_thread(impl)
                
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        # TODO: implementing this by using IModelCenter.parallelInstance() instead of limiting the user
        # to a single open workflow. Might not be needed if we just want to error if multiple workflows
        # are loaded. Doing this has implications on the UI functions.
        def impl() -> IWorkflowInstance:
            # parallelInstance() returns a plain IDispatch. We want an IModelCenter. I tried
            # LOTS of ways and this was the only one that I could find that works. Pass the _oleobj_ 
            # of the IDispatch to the IModelCenter constructor. We will need to use this pattern
            # all over the place.
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
     
