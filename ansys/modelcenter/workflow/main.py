# Copyright (c) 2022, Ansys Inc. Unauthorised use, distribution or duplication is prohibited

from ansys.modelcenter.workflow.desktop import ModelCenter

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    instance = ModelCenter()
    version = instance.version
    print("ModelCenter version: " + version)
    instance = None
