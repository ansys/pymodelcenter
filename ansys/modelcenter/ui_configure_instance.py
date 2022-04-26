from typing import Tuple


class UIConfigureInstance:
    """
    Collection of methods that can change UI related configuration on
    an instance, but does not require an active UI to operate.
    """
    def __init__(self):
        pass

    # void setAssemblyStyle(
    #   BSTR assemblyName, AssemblyStyle style, [optional]VARIANT width, [optional]VARIANT height);
    def set_assembly_style(
            self,
            assembly_name: str,
            style: object,
            width: object = None,
            height: object = None) -> None:
        pass

    # AssemblyStyle getAssemblyStyle(BSTR assemblyName, int *width, int *height);
    def get_assembly_style(self, assembly_name) -> Tuple[int, int]:
        pass
