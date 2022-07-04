"""Definition of common base for any type which uses custom metadata."""
from typing import Any, Optional, Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element as XMLElement
from xml.etree.ElementTree import ParseError as XMLParseError

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.utils.implicit_coercion import implicit_coerce
import clr

from ansys.modelcenter.workflow.api.component_metadata import (
    ComponentMetadataAccess,
    ComponentMetadataType,
)
from ansys.modelcenter.workflow.api.i18n import i18n

clr.AddReference("phoenix-mocks/Interop.ModelCenter")
from ModelCenter import IAssembly as mcapiIAssembly  # type: ignore
from ModelCenter import IComponent as mcapiIComponent  # type: ignore
from ModelCenter import IVariable as mcapiIVariable  # type: ignore


class _MetadataValueVisitor(acvi.IVariableValueVisitor[ComponentMetadataType]):
    """
    Visits a Python Ansys Common Variable Interop value and converts it to the simple Python value.

    File and array values are not supported.
    """

    def __init__(self):
        self._value: Any = None

    @property
    def value(self) -> Any:
        return self._value

    def visit_integer(self, value: acvi.IntegerValue) -> ComponentMetadataType:
        self._value = int(value)
        return ComponentMetadataType.LONG

    def visit_real(self, value: acvi.RealValue) -> ComponentMetadataType:
        self._value = float(value)
        return ComponentMetadataType.DOUBLE

    def visit_boolean(self, value: acvi.BooleanValue) -> ComponentMetadataType:
        self._value = bool(value)
        return ComponentMetadataType.BOOLEAN

    def visit_string(self, value: acvi.StringValue) -> ComponentMetadataType:
        self._value = str(value)
        return ComponentMetadataType.STRING

    def visit_file(self, value: acvi.FileValue) -> ComponentMetadataType:
        pass

    def visit_integer_array(self, value: acvi.IntegerArrayValue) -> ComponentMetadataType:
        pass

    def visit_real_array(self, value: acvi.RealArrayValue) -> ComponentMetadataType:
        pass

    def visit_boolean_array(self, value: acvi.BooleanArrayValue) -> ComponentMetadataType:
        pass

    def visit_string_array(self, value: acvi.StringArrayValue) -> ComponentMetadataType:
        pass

    def visit_file_array(self, value: acvi.FileArrayValue) -> ComponentMetadataType:
        pass


class CustomMetadataOwner:
    """Common base for any class which uses custom metadata."""

    InstanceType = Union[mcapiIAssembly, mcapiIComponent, mcapiIVariable]
    """Possible types which CustomMetadataOwner can currently wrap."""

    def __init__(self, instance: InstanceType):
        """
        Initialize a new instance.

        Parameters
        ----------
        instance : mcapiIAssembly, mcapiIComponent, or mcapiIVariable
            The raw MCAPI interface object to use to make direct calls
            to ModelCenter.
        """
        self._wrapped = instance

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
        meta_type: ComponentMetadataType
        if isinstance(value, str):
            meta_type = ComponentMetadataType.STRING
        elif isinstance(value, float):
            meta_type = ComponentMetadataType.DOUBLE
        elif isinstance(value, bool):
            # It's important that this comes before int, as python bool is a subclass of int.
            meta_type = ComponentMetadataType.BOOLEAN
        elif isinstance(value, int):
            meta_type = ComponentMetadataType.LONG
        elif isinstance(value, XMLElement):
            meta_type = ComponentMetadataType.XML
            value = ElementTree.tostring(value).decode("utf-8")
        else:
            raise TypeError(i18n("Exceptions", "ERROR_METADATA_TYPE_NOT_ALLOWED"))

        return self._wrapped.setMetadata(name, meta_type.value, value, access.value, archive)

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
        ret = self._wrapped.getMetadata(name)
        if isinstance(ret, str):
            ret_len = len(ret)
            # if it looks like it might be XML
            if ret_len > 2 and ret[0] == "<" and ret[ret_len - 1] == ">":
                try:
                    xml = ElementTree.fromstring(ret)
                    ret = xml
                except XMLParseError:
                    pass
        return ret

    def set_custom_metadata_value(self, name: str, value: acvi.IVariableValue) -> None:
        """
        Set metadata value of the given named metadata.

        Parameters
        ----------
        name :
            Metadata specifier used to store the data.
        value : IVariableValue
            The value of the metadata item.
        """
        visitor = _MetadataValueVisitor()
        meta_type: ComponentMetadataType = value.accept(visitor)

        if visitor.value is None:
            raise TypeError(i18n("Exceptions", "ERROR_METADATA_TYPE_NOT_ALLOWED"))

        self._wrapped.setMetadata(
            name, meta_type.value, visitor.value, ComponentMetadataAccess.PUBLIC.value, True
        )

    def get_custom_metadata_value(self, name: str) -> Optional[acvi.IVariableValue]:
        """
        Get the named metadata as a `Property` object.

        Parameters
        ----------
        name :
            Metadata key name.

        Returns
        -------
        `Property` object or ``None`` if metadata not found.
        """
        value: Optional[acvi.IVariableValue] = None
        metadata = self._wrapped.getMetadata(name)
        if metadata is not None:
            value = self.__interop_value(metadata)
        return value

    @implicit_coerce
    def __interop_value(self, value: acvi.IVariableValue) -> acvi.IVariableValue:
        """Convert common Python values to interop value."""
        return value
