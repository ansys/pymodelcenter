# Copyright (c) 2022, Ansys Inc. Unauthorised use, distribution or duplication is prohibited
import trio
from ansys.modelcenter.desktop import ModelCenter
from ansys.common.variableinterop import *
from ansys.engineeringworkflow.api import *

async def main():
    instance = ModelCenter()
    await instance.initialize()
    version = instance.version
    print("ModelCenter version: " + version)
    print(await instance.get_server_info())
    
    wf = await instance.load_workflow("c:\\Users\\nsharp\\Desktop\\delme.pxcz")
    print(await wf.run({"Model.QuickWrap5.a": VariableState(True, RealValue(3.2))}, False, ["Model.QuickWrap5.b"]))
    instance = None
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trio.run(main)