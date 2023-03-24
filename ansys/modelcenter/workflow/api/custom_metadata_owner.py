"""Definition of common base for any type which uses custom metadata."""
from abc import ABC, abstractmethod
from typing import Union
from xml.etree.ElementTree import Element as XMLElement

from ansys.modelcenter.workflow.api.component_metadata import ComponentMetadataAccess


class ICustomMetadataOwner(ABC):
    """Common base for any class which uses custom metadata."""

    # TODO/REDUCE: Consider removing the XMLElement support.
    # TODO/REDUCE: Consider removing ComponentMetadataAccess field
    #   - only allow creating / setting public metadata.
    # TODO: I'm pretty sure the archive property is not correctly documented here.
    @abstractmethod
    def set_custom_metadata(
        self,
        name: str,
        value: Union[str, int, float, bool, XMLElement],
        access: ComponentMetadataAccess,
        archive: bool,
    ) -> None:
        """
        Set metadata value of the given named metadata.

        Parameters
        ----------
        name :
            Metadata specifier used to store the data.
        value : Union[str, float, bool, int, XMLElement]
            The value of the metadata item.
        access : ComponentMetadataAccess
            The level of access allowed to the metadata.
        archive : bool
            Whether the metadata should be considered archived.
        """
        raise NotImplementedError()

    # TODO/REDUCE: Consider removing XMLElement support.
    #       Existing XML properties will return as str.
    @abstractmethod
    def get_custom_metadata(self, name: str) -> Union[str, int, float, bool, XMLElement]:
        """
        Get the named metadata.

        Parameters
        ----------
        name :
            Metadata key name.

        Returns
        -------
        Metadata value.
        """
        raise NotImplementedError()

    # TODO: No delete metadata?
    #       The COM API doesn't have it either, strangely ...
