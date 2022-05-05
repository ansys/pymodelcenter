from typing import Union

from ansys.modelcenter.workflow.api.component_metadata import (
    ComponentMetadataAccess,
    ComponentMetadataType
)
from ansys.modelcenter.workflow.api.i18n import i18n
import clr

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IAssembly as mcapiIAssembly
from ModelCenter import IComponent as mcapiIComponent
from ModelCenter import IVariable as mcapiIVariable

class MetadataOwner:

    def __init__(self, instance: Union[mcapiIAssembly, mcapiIComponent, mcapiIVariable]):
        """
        Initialize a new instance.

        Parameters
        ----------
        instance : mcapiIAssembly, mcapiIComponent, or mcapiIVariable
            The raw MCAPI interface object ot use to make direct calls
            to ModelCenter.
        """
        self._instance = instance

    def set_metadata(self,
                     name: str,
                     value: Union[str, int, float, bool],
                     access: ComponentMetadataAccess,
                     archive: bool,
                     value_is_xml: bool = False) -> None:
        """
        Sets the metadata value of the given metadata key name.

        Parameters
        ----------
        name :
            Metadata specifier used to store the data.
        value :
            The value of the metadata item.
        access :
            The level of access allowed to the metadata.
        archive :
            Whether the metadata should be considered archived.
        value_is_xml :
            Whether the metadata value is XML. This should be used
            only when passing a string containing XML that should be interpreted as such.
        """
        meta_type: ComponentMetadataType = ComponentMetadataType.STRING
        if isinstance(value, str):
            meta_type = ComponentMetadataType.STRING
            if value_is_xml:
                meta_type = ComponentMetadataType.XML
        elif isinstance(value, float):
            meta_type = ComponentMetadataType.DOUBLE
        elif isinstance(value, bool):
            # It's important that this comes before int, as python bool is a subclass of int.
            meta_type = ComponentMetadataType.BOOLEAN
        elif isinstance(value, int):
            meta_type = ComponentMetadataType.LONG
        else:
            raise TypeError(i18n('Exceptions', 'ERROR_METADATA_TYPE_NOT_ALLOWED'))

        return self._instance.setMetadata(name, meta_type.value, value, access.value, archive)

    def get_metadata(self, name: str) -> object:    # Metadata
        """
        Gets the meta data value of the given meta data key name.

        Parameters
        ----------
        name :
            Metadata key name.

        Returns
        -------
        Metadata value.
        """
        # VARIANT getMetadata(BSTR name);
        return self._instance.getMetadata(name)