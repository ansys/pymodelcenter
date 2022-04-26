# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)]
# From type library 'ModelCenterTypeLibrary64.exe'
# On Tue Mar 15 15:51:32 2022
'Phoenix Integration - ModelCenter'
makepy_version = '0.5.01'
python_version = 0x30a02f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{757DD9B4-E5E1-11D2-81A3-0060975E6478}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
	ASSEMBLY_STYLE_AUTO_N_SQUARED =102        # from enum AssemblyStyle
	ASSEMBLY_STYLE_CLASSIC        =100        # from enum AssemblyStyle
	ASSEMBLY_STYLE_COLLAPSED      =0          # from enum AssemblyStyle
	ASSEMBLY_STYLE_EXPANDED       =1          # from enum AssemblyStyle
	ASSEMBLY_STYLE_FORCE_32_BITS  =65536      # from enum AssemblyStyle
	ASSEMBLY_STYLE_N_SQUARED      =101        # from enum AssemblyStyle
	METADATA_ACCESS_FORCE_TO_32_BITS=65536      # from enum MetadataAccess
	METADATA_ACCESS_PRIVATE       =0          # from enum MetadataAccess
	METADATA_ACCESS_PUBLIC        =2          # from enum MetadataAccess
	METADATA_ACCESS_READONLY      =1          # from enum MetadataAccess
	METADATA_TYPE_BOOLEAN         =3          # from enum MetadataType
	METADATA_TYPE_DOUBLE          =1          # from enum MetadataType
	METADATA_TYPE_FORCE_TO_32_BITS=65536      # from enum MetadataType
	METADATA_TYPE_LONG            =2          # from enum MetadataType
	METADATA_TYPE_STRING          =0          # from enum MetadataType
	METADATA_TYPE_XML             =4          # from enum MetadataType
	CONN_ERR_ERROR                =3          # from enum OnConnectionErrorMode
	CONN_ERR_IGNORE               =1          # from enum OnConnectionErrorMode
	CONN_ERR_USEDIALOG            =-1         # from enum OnConnectionErrorMode
	TS_FORMAT_PXTZ                =0          # from enum TradeStudyFormat
	TS_FORMAT_PXT_COMPRESSED      =1          # from enum TradeStudyFormat
	TS_FORMAT_PXT_UNCOMPRESSED    =2          # from enum TradeStudyFormat
	TS_FORMAT_TSTUDY              =3          # from enum TradeStudyFormat
	DO_NOT_VERSION                =1          # from enum VersionStatus
	DO_VERSIONING                 =0          # from enum VersionStatus
	DO_VERSIONING_IF_POSSIBLE     =2          # from enum VersionStatus

from win32com.client import DispatchBaseClass
class IAddToModel(DispatchBaseClass):
	'AddToModel object'
	CLSID = IID('{6B3DCC47-6475-411C-977E-337F73A43771}')
	coclass_clsid = None

	def addInput(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), ((8, 0), (8, 0), (12, 16)),name
			, type, value)
		if ret is not None:
			ret = Dispatch(ret, 'addInput', None)
		return ret

	def addInput2(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, classURL=defaultNamedNotOptArg, value=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(20, LCID, 1, (9, 0), ((8, 0), (8, 0), (8, 0), (12, 16)),name
			, type, classURL, value)
		if ret is not None:
			ret = Dispatch(ret, 'addInput2', None)
		return ret

	def addMethod(self, name=defaultNamedNotOptArg, displayName=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), ((8, 0), (12, 16)),name
			, displayName)

	def addOutput(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), ((8, 0), (8, 0), (12, 16)),name
			, type, value)
		if ret is not None:
			ret = Dispatch(ret, 'addOutput', None)
		return ret

	def addOutput2(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, classURL=defaultNamedNotOptArg, value=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(21, LCID, 1, (9, 0), ((8, 0), (8, 0), (8, 0), (12, 16)),name
			, type, classURL, value)
		if ret is not None:
			ret = Dispatch(ret, 'addOutput2', None)
		return ret

	def addToModel(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (),)

	def addToModel2(self):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (11, 0), (),)

	def addToModel3(self, suggestedName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(22, LCID, 1, (8, 0), ((8, 0),),suggestedName
			)

	def clearBusyFlag(self):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (24, 0), (),)

	def getComponent(self):
		ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getComponent', None)
		return ret

	def getProgID(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def getRegID(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def setAuthor(self, author=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), ((8, 0),),author
			)

	def setComponentRequirements(self, compReq=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), ((8, 0),),compReq
			)

	def setDescription(self, description=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), ((8, 0),),description
			)

	def setHelpURL(self, helpURL=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), ((8, 0),),helpURL
			)

	def setIcon(self, iconFile=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (24, 0), ((8, 0),),iconFile
			)

	def setKeywords(self, keywords=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (24, 0), ((8, 0),),keywords
			)

	def setVersion(self, version=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), ((8, 0),),version
			)

	def updateComponent(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"autoRun": (8, 2, (11, 0), (), "autoRun", None),
		"prevalidateInputs": (7, 2, (11, 0), (), "prevalidateInputs", None),
	}
	_prop_map_put_ = {
		"autoRun" : ((8, LCID, 4, 0),()),
		"prevalidateInputs" : ((7, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IArray(DispatchBaseClass):
	'Array base class'
	CLSID = IID('{6CBF1A48-679A-11D3-A518-00A024B5452E}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getDimensions(self):
		return self._ApplyTypes_(1013, 1, (12, 0), (), 'getDimensions', None,)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getSize(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1011, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setSize(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1012, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"autoSize": (1005, 2, (11, 0), (), "autoSize", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"length": (1010, 2, (3, 0), (), "length", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"autoSize" : ((1005, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"length" : ((1010, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IAssemblies(DispatchBaseClass):
	'Assemblies object'
	CLSID = IID('{0D132C3C-CA70-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	def Item(self, id=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (12, 0), ((12, 0),), 'Item', None,id
			)

	_prop_map_get_ = {
		"Count": (1, 2, (12, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 1, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (12, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IAssembly(DispatchBaseClass):
	'Assembly'
	CLSID = IID('{0D132C36-CA70-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	def addAssembly(self, name=defaultNamedNotOptArg, AssemblyType=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(7, LCID, 1, (9, 0), ((8, 0), (12, 16)),name
			, AssemblyType)
		if ret is not None:
			ret = Dispatch(ret, 'addAssembly', None)
		return ret

	def addAssembly2(self, name=defaultNamedNotOptArg, xPos=defaultNamedNotOptArg, yPos=defaultNamedNotOptArg, AssemblyType=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((8, 0), (12, 0), (12, 0), (12, 16)),name
			, xPos, yPos, AssemblyType)
		if ret is not None:
			ret = Dispatch(ret, 'addAssembly2', None)
		return ret

	def addVariable(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(8, LCID, 1, (9, 0), ((8, 0), (8, 0)),name
			, type)
		if ret is not None:
			ret = Dispatch(ret, 'addVariable', None)
		return ret

	def convertToSubmodel(self, fileName=defaultNamedNotOptArg, VersionStatus=defaultNamedNotOptArg, checkinMessage=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), ((8, 0), (3, 0), (8, 0)),fileName
			, VersionStatus, checkinMessage)

	def deleteVariable(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), ((8, 0),),name
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(21, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getPositionX(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), (),)

	def getPositionY(self):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), (),)

	def rename(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), ((8, 0),),name
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	_prop_map_get_ = {
		"Assemblies": (3, 2, (12, 0), (), "Assemblies", None),
		"AssemblyType": (17, 2, (8, 0), (), "AssemblyType", None),
		"Components": (4, 2, (12, 0), (), "Components", None),
		"Groups": (2, 2, (12, 0), (), "Groups", None),
		"IndexInParent": (15, 2, (3, 0), (), "IndexInParent", None),
		"ParentAssembly": (16, 2, (9, 0), (), "ParentAssembly", None),
		"Variables": (1, 2, (12, 0), (), "Variables", None),
		"iconID": (9, 2, (3, 0), (), "iconID", None),
		"userData": (18, 2, (12, 0), (), "userData", None),
	}
	_prop_map_put_ = {
		"Assemblies" : ((3, LCID, 4, 0),()),
		"AssemblyType" : ((17, LCID, 4, 0),()),
		"Components" : ((4, LCID, 4, 0),()),
		"Groups" : ((2, LCID, 4, 0),()),
		"IndexInParent" : ((15, LCID, 4, 0),()),
		"ParentAssembly" : ((16, LCID, 4, 0),()),
		"Variables" : ((1, LCID, 4, 0),()),
		"iconID" : ((9, LCID, 4, 0),()),
		"userData" : ((18, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IBooleanArray(DispatchBaseClass):
	'Boolean variable array'
	CLSID = IID('{6CBF1A4F-679A-11D3-A518-00A024B5452E}')
	coclass_clsid = None

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (3, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getArray(self):
		return self._ApplyTypes_(2005, 1, (12, 0), (), 'getArray', None,)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getValue(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2003, LCID, 1, (11, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def getValueAbsolute(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2007, LCID, 1, (11, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setArray(self, array=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2006, LCID, 1, (24, 0), ((12, 0),),array
			)

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setValue(self, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2004, LCID, 1, (24, 0), ((3, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),value
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (11, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (2002, 2, (8, 0), (), "description", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((2002, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (11, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IBooleanVariable(DispatchBaseClass):
	'Boolean variable'
	CLSID = IID('{985910EA-C34D-11D2-A4E8-00A024B5452E}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setInitialValue(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((3, 0),),value
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1002, 2, (8, 0), (), "description", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"value": (1001, 2, (11, 0), (), "value", None),
		"valueAbsolute": (1004, 2, (11, 0), (), "valueAbsolute", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1002, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
		"valueAbsolute" : ((1004, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (11, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICachePin(DispatchBaseClass):
	'CachePin'
	CLSID = IID('{631F5771-6F41-495F-BF88-55368128C415}')
	coclass_clsid = None

	def checkinOnFlush(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((8, 0),),message
			)

	def releasePin(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

	_prop_map_get_ = {
		"LocalPath": (2, 2, (8, 0), (), "LocalPath", None),
		"isValid": (3, 2, (11, 0), (), "isValid", None),
		"url": (1, 2, (8, 0), (), "url", None),
	}
	_prop_map_put_ = {
		"LocalPath" : ((2, LCID, 4, 0),()),
		"isValid" : ((3, LCID, 4, 0),()),
		"url" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IComponent(DispatchBaseClass):
	'Component'
	CLSID = IID('{526AC1E1-D718-11D3-A544-00A024B5452E}')
	coclass_clsid = None

	def downloadValues(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(22, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (),)

	def getPositionX(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), (),)

	def getPositionY(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), (),)

	def getSource(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17, LCID, 1, (8, 0), (),)

	def getVariable(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariable', None)
		return ret

	def invalidate(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def invokeMethod(self, method=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((8, 0),),method
			)

	def reconnect(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def rename(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (24, 0), ((8, 0),),name
			)

	def run(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def show(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"AssociatedFiles": (15, 2, (12, 0), (), "AssociatedFiles", None),
		"Groups": (6, 2, (12, 0), (), "Groups", None),
		"IndexInParent": (18, 2, (3, 0), (), "IndexInParent", None),
		"ParentAssembly": (19, 2, (9, 0), (), "ParentAssembly", None),
		"Variables": (5, 2, (12, 0), (), "Variables", None),
		"userData": (11, 2, (12, 0), (), "userData", None),
	}
	_prop_map_put_ = {
		"AssociatedFiles" : ((15, LCID, 4, 0),()),
		"Groups" : ((6, LCID, 4, 0),()),
		"IndexInParent" : ((18, LCID, 4, 0),()),
		"ParentAssembly" : ((19, LCID, 4, 0),()),
		"Variables" : ((5, LCID, 4, 0),()),
		"userData" : ((11, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IComponents(DispatchBaseClass):
	'Components object'
	CLSID = IID('{712469FD-A1E9-4450-BE93-457ED13A91F1}')
	coclass_clsid = None

	def Item(self, id=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (12, 0), ((12, 0),), 'Item', None,id
			)

	_prop_map_get_ = {
		"Count": (1, 2, (12, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 1, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (12, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class ICustomDesignPoint(DispatchBaseClass):
	'Data Collector Custom Design Point object'
	CLSID = IID('{214FB734-840B-4BC1-A063-1D2DFA0C6D0A}')
	coclass_clsid = None

	def addVariable(self, name=defaultNamedNotOptArg, equation=defaultNamedNotOptArg, isNumeric=defaultNamedNotOptArg, isValid=defaultNamedNotOptArg
			, isInput=defaultNamedNotOptArg, type=defaultNamedNotOptArg, units=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((8, 0), (8, 0), (3, 0), (3, 0), (3, 0), (8, 0), (8, 0), (8, 0)),name
			, equation, isNumeric, isValid, isInput, type
			, units, value)

	def runFailed(self, reason=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((8, 0),),reason
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IDataCollector(DispatchBaseClass):
	'Data Collector object'
	CLSID = IID('{1539CF41-7B1A-11D3-A526-00A024B5452E}')
	coclass_clsid = None

	def addCustom(self, variable=defaultNamedNotOptArg, label=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((8, 0), (8, 0)),variable
			, label)

	def createEmptyRuns(self, numEmptyRuns=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((3, 0),),numEmptyRuns
			)

	def enableCarpetPlotTab(self, var1=defaultNamedNotOptArg, var2=defaultNamedNotOptArg, plotVar=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0)),var1
			, var2, plotVar)

	def enableGraphTab(self, flag=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((3, 0),),flag
			)

	def enableMainEffectsTab(self):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), (),)

	def endRuns(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def exportToCSV(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def fromString(self, str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0),),str
			)

	def getDataExplorer(self):
		ret = self._oleobj_.InvokeTypes(28, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getDataExplorer', None)
		return ret

	def getErrorID(self, run=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((3, 0),),run
			)

	def getErrorMessage(self, run=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(12, LCID, 1, (8, 0), ((3, 0),),run
			)

	def getNumFailedRuns(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), (),)

	def getNumRuns(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), (),)

	def getNumVariables(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), (),)

	def getValue(self, index=defaultNamedNotOptArg, run=defaultNamedNotOptArg):
		return self._ApplyTypes_(15, 1, (12, 0), ((12, 0), (3, 0)), 'getValue', None,index
			, run)

	def getVariableDescription(self, index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 0),),index
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariableDescription', None)
		return ret

	def hide(self):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), (),)

	def isValid(self, index=defaultNamedNotOptArg, run=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (3, 0), ((12, 0), (3, 0)),index
			, run)

	def newCustomDesignPoint(self):
		ret = self._oleobj_.InvokeTypes(26, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'newCustomDesignPoint', None)
		return ret

	def save(self, fileName=defaultNamedNotOptArg, displayName=defaultNamedNotOptArg, description=defaultNamedNotOptArg, author=defaultNamedNotOptArg
			, saveModel=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0), (8, 0), (3, 0)),fileName
			, displayName, description, author, saveModel)

	def selectX(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((8, 0),),name
			)

	def selectY(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((8, 0),),name
			)

	def setCustomRun(self, index=defaultNamedNotOptArg, customDesignPoint=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), ((3, 0), (9, 0)),index
			, customDesignPoint)

	def setNumExpectedRuns(self, numRuns=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((3, 0),),numRuns
			)

	def show(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def startRuns(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def storeCurrentDesignPoint(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (),)

	def storeCustomDesignPoint(self, customDesignPoint=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), ((9, 0),),customDesignPoint
			)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), (),)

	_prop_map_get_ = {
		"isVisible": (30, 2, (3, 0), (), "isVisible", None),
	}
	_prop_map_put_ = {
		"isVisible" : ((30, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IDataMonitor(DispatchBaseClass):
	'Data Monitor object'
	CLSID = IID('{B4009E4E-5E90-4B44-8687-143051AA7400}')
	coclass_clsid = None

	def addItem(self, name=defaultNamedNotOptArg, link=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), ((8, 0), (8, 0)),name
			, link)

	def addUnlinkedItem(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), ((8, 0),),name
			)

	def getAutoDelete(self):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), (),)

	def getColWidth(self, col=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), ((3, 0),),col
			)

	def getDisplayFullNames(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (11, 0), (),)

	def getDisplayUnits(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (11, 0), (),)

	def getHeight(self):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), (),)

	def getLink(self, row=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), ((3, 0),),row
			)

	def getName(self, row=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), ((3, 0),),row
			)

	def getTitle(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(19, LCID, 1, (8, 0), (),)

	def getWidth(self):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (3, 0), (),)

	def getX(self):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), (),)

	def getY(self):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (3, 0), (),)

	def isRenamed(self, row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((3, 0),),row
			)

	def isValid(self):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (11, 0), (),)

	def removeItem(self, row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((3, 0),),row
			)

	def removeLink(self, row=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), ((3, 0),),row
			)

	def setAutoDelete(self, _MIDL__IDataMonitor0001_=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), ((11, 0),),_MIDL__IDataMonitor0001_
			)

	def setColWidth(self, col=defaultNamedNotOptArg, width=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), ((3, 0), (3, 0)),col
			, width)

	def setDisplayFullNames(self, _MIDL__IDataMonitor0000_=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), ((11, 0),),_MIDL__IDataMonitor0000_
			)

	def setDisplayUnits(self, _MIDL__IDataMonitor0002_=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (24, 0), ((11, 0),),_MIDL__IDataMonitor0002_
			)

	def setLink(self, row=defaultNamedNotOptArg, link=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((3, 0), (8, 0)),row
			, link)

	def setLocation(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (24, 0), ((3, 0), (3, 0)),x
			, y)

	def setName(self, row=defaultNamedNotOptArg, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((3, 0), (8, 0)),row
			, name)

	def setSize(self, width=defaultNamedNotOptArg, height=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), ((3, 0), (3, 0)),width
			, height)

	def setTitle(self, title=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((8, 0),),title
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IDoubleArray(DispatchBaseClass):
	'Double variable array'
	CLSID = IID('{514D1080-6A11-11D3-A518-00A024B5452E}')
	coclass_clsid = None

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (5, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	def clearLowerBound(self):
		return self._oleobj_.InvokeTypes(2019, LCID, 1, (24, 0), (),)

	def clearUpperBound(self):
		return self._oleobj_.InvokeTypes(2018, LCID, 1, (24, 0), (),)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFormattedStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2016, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getArray(self):
		return self._ApplyTypes_(2012, 1, (12, 0), (), 'getArray', None,)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getValue(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2010, LCID, 1, (5, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def getValueAbsolute(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2020, LCID, 1, (5, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def hasLowerBound(self):
		return self._oleobj_.InvokeTypes(2008, LCID, 1, (11, 0), (),)

	def hasUpperBound(self):
		return self._oleobj_.InvokeTypes(2009, LCID, 1, (11, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setArray(self, array=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2013, LCID, 1, (24, 0), ((12, 0),),array
			)

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setValue(self, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2011, LCID, 1, (24, 0), ((5, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),value
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def toFormattedStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2017, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toFormattedStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2015, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (5, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (2004, 2, (8, 0), (), "description", None),
		"enumAliases": (2006, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (2007, 2, (8, 0), (), "enumValues", None),
		"format": (2014, 2, (8, 0), (), "format", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"lowerBound": (2002, 2, (5, 0), (), "lowerBound", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
		"units": (2005, 2, (8, 0), (), "units", None),
		"upperBound": (2003, 2, (5, 0), (), "upperBound", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((2004, LCID, 4, 0),()),
		"enumAliases" : ((2006, LCID, 4, 0),()),
		"enumValues" : ((2007, LCID, 4, 0),()),
		"format" : ((2014, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"lowerBound" : ((2002, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
		"units" : ((2005, LCID, 4, 0),()),
		"upperBound" : ((2003, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (5, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IDoubleVariable(DispatchBaseClass):
	'Double variable'
	CLSID = IID('{985910E7-C34D-11D2-A4E8-00A024B5452E}')
	coclass_clsid = None

	def clearLowerBound(self):
		return self._oleobj_.InvokeTypes(1016, LCID, 1, (24, 0), (),)

	def clearUpperBound(self):
		return self._oleobj_.InvokeTypes(1015, LCID, 1, (24, 0), (),)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFormattedString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1013, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def hasLowerBound(self):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (11, 0), (),)

	def hasUpperBound(self):
		return self._oleobj_.InvokeTypes(1010, LCID, 1, (11, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setInitialValue(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((5, 0),),value
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toFormattedString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1012, LCID, 1, (8, 0), (),)

	def toFormattedStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1014, LCID, 1, (8, 0), (),)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1005, 2, (8, 0), (), "description", None),
		"enumAliases": (1007, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (1006, 2, (8, 0), (), "enumValues", None),
		"format": (1011, 2, (8, 0), (), "format", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"lowerBound": (1002, 2, (5, 0), (), "lowerBound", None),
		"units": (1004, 2, (8, 0), (), "units", None),
		"upperBound": (1003, 2, (5, 0), (), "upperBound", None),
		"value": (1001, 2, (5, 0), (), "value", None),
		"valueAbsolute": (1017, 2, (5, 0), (), "valueAbsolute", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1005, LCID, 4, 0),()),
		"enumAliases" : ((1007, LCID, 4, 0),()),
		"enumValues" : ((1006, LCID, 4, 0),()),
		"format" : ((1011, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"lowerBound" : ((1002, LCID, 4, 0),()),
		"units" : ((1004, LCID, 4, 0),()),
		"upperBound" : ((1003, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
		"valueAbsolute" : ((1017, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (5, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IFeature(DispatchBaseClass):
	'FlexLM Feature'
	CLSID = IID('{22D5CD66-AF6F-48F7-AC03-80095DE85C94}')
	coclass_clsid = None

	def checkin(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IFileArray(DispatchBaseClass):
	'File variable array'
	CLSID = IID('{14F18BD0-5BD9-4FCC-B084-7D95360631BE}')
	coclass_clsid = None

	# The method SetfileExtension is actually a property, but must be used as a method to correctly pass the arguments
	def SetfileExtension(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2006, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (8, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (8, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	# The method fileExtension is actually a property, but must be used as a method to correctly pass the arguments
	def fileExtension(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2006, LCID, 2, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def fromFile(self, fileName=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2008, LCID, 1, (24, 0), ((8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),fileName
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getFileExtension(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2004, LCID, 1, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setFileExtension(self, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2005, LCID, 1, (24, 0), ((8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),value
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toFile(self, fileName=defaultNamedNotOptArg, encoding=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg
			, d3=defaultNamedOptArg, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg
			, d8=defaultNamedOptArg, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2007, LCID, 1, (24, 0), ((8, 0), (12, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),fileName
			, encoding, d1, d2, d3, d4
			, d5, d6, d7, d8, d9
			, d10)

	def toFileAbsolute(self, fileName=defaultNamedNotOptArg, encoding=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg
			, d3=defaultNamedOptArg, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg
			, d8=defaultNamedOptArg, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2011, LCID, 1, (24, 0), ((8, 0), (12, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),fileName
			, encoding, d1, d2, d3, d4
			, d5, d6, d7, d8, d9
			, d10)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (2003, 2, (8, 0), (), "description", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"isBinary": (2002, 2, (11, 0), (), "isBinary", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"saveWithModel": (2013, 2, (11, 0), (), "saveWithModel", None),
		"size": (1001, 2, (3, 0), (), "size", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((2003, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"isBinary" : ((2002, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"saveWithModel" : ((2013, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IFileSystemInfo(DispatchBaseClass):
	'FileSystemInfo'
	CLSID = IID('{3E645325-85F9-456B-B5B7-395C90825986}')
	coclass_clsid = None

	def pin(self, forWrite=defaultNamedNotOptArg, forceCopy=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(6, LCID, 1, (9, 0), ((11, 0), (12, 16)),forWrite
			, forceCopy)
		if ret is not None:
			ret = Dispatch(ret, 'pin', None)
		return ret

	_prop_map_get_ = {
		"baseName": (4, 2, (8, 0), (), "baseName", None),
		"exists": (2, 2, (11, 0), (), "exists", None),
		"isValid": (1, 2, (11, 0), (), "isValid", None),
		"isWritable": (3, 2, (11, 0), (), "isWritable", None),
		"url": (5, 2, (8, 0), (), "url", None),
	}
	_prop_map_put_ = {
		"baseName" : ((4, LCID, 4, 0),()),
		"exists" : ((2, LCID, 4, 0),()),
		"isValid" : ((1, LCID, 4, 0),()),
		"isWritable" : ((3, LCID, 4, 0),()),
		"url" : ((5, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IFileVariable(DispatchBaseClass):
	'File variable'
	CLSID = IID('{A79BA2F2-C8C2-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFile(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1005, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def readFile(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toFile(self, fileName=defaultNamedNotOptArg, encoding=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (24, 0), ((8, 0), (12, 16)),fileName
			, encoding)

	def toFileAbsolute(self, fileName=defaultNamedNotOptArg, encoding=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((8, 0), (12, 16)),fileName
			, encoding)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	def writeFile(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1006, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def writeFileAbsolute(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1010, 2, (8, 0), (), "description", None),
		"directTransfer": (1012, 2, (11, 0), (), "directTransfer", None),
		"fileExtension": (1003, 2, (8, 0), (), "fileExtension", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"isBinary": (1002, 2, (11, 0), (), "isBinary", None),
		"saveWithModel": (1011, 2, (11, 0), (), "saveWithModel", None),
		"value": (1001, 2, (8, 0), (), "value", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1010, LCID, 4, 0),()),
		"directTransfer" : ((1012, LCID, 4, 0),()),
		"fileExtension" : ((1003, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"isBinary" : ((1002, LCID, 4, 0),()),
		"saveWithModel" : ((1011, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (8, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IGeometryVariable(DispatchBaseClass):
	'Geometry variable'
	CLSID = IID('{E45A67F4-C367-11D2-A4E8-00A024B5452E}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setInitialValue(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0),),value
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1002, 2, (8, 0), (), "description", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"value": (1001, 2, (8, 0), (), "value", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1002, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (8, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IGlobalParameters(DispatchBaseClass):
	CLSID = IID('{CBBF5B6F-ED70-463D-B1E6-6DAE10500A4E}')
	coclass_clsid = None

	# The method Item is actually a property, but must be used as a method to correctly pass the arguments
	def Item(self, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(4, 2, (12, 0), ((12, 0),), 'Item', None,index
			)

	def Remove(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 0),),index
			)

	# The method SetItem is actually a property, but must be used as a method to correctly pass the arguments
	def SetItem(self, index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(4, LCID, 4, (24, 0), ((12, 0), (12, 0)),index
			, arg1)

	# The method Set_item is actually a property, but must be used as a method to correctly pass the arguments
	def Set_item(self, index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(0, LCID, 4, (24, 0), ((12, 0), (12, 0)),index
			, arg1)

	# The method _item is actually a property, but must be used as a method to correctly pass the arguments
	def _item(self, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(0, 2, (12, 0), ((12, 0),), '_item', None,index
			)

	def setExportToRemoteComponents(self, index=defaultNamedNotOptArg, bexport=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 0), (11, 0)),index
			, bexport)

	_prop_map_get_ = {
		"Count": (1, 2, (3, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	# Default method for this class is '_item'
	def __call__(self, index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(0, LCID, 4, (24, 0), ((12, 0), (12, 0)),index
			, arg1)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(4, LCID, 2, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IGroup(DispatchBaseClass):
	'Group'
	CLSID = IID('{0D132C39-CA70-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	_prop_map_get_ = {
		"Groups": (2, 2, (12, 0), (), "Groups", None),
		"Variables": (1, 2, (12, 0), (), "Variables", None),
		"iconID": (5, 2, (3, 0), (), "iconID", None),
	}
	_prop_map_put_ = {
		"Groups" : ((2, LCID, 4, 0),()),
		"Variables" : ((1, LCID, 4, 0),()),
		"iconID" : ((5, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IGroups(DispatchBaseClass):
	'Groups object'
	CLSID = IID('{0D132C3F-CA70-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	def Item(self, id=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (12, 0), ((12, 0),), 'Item', None,id
			)

	_prop_map_get_ = {
		"Count": (1, 2, (12, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 1, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (12, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IIfComponent(DispatchBaseClass):
	'If component'
	CLSID = IID('{897C0864-810E-444A-B648-F6F08C639BC3}')
	coclass_clsid = None

	def downloadValues(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def getBranchCondition(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getBranchName(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1006, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), (),)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (),)

	def getNumBranches(self):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (3, 0), (),)

	def getPositionX(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), (),)

	def getPositionY(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), (),)

	def getSource(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17, LCID, 1, (8, 0), (),)

	def getVariable(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariable', None)
		return ret

	def invalidate(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def invokeMethod(self, method=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((8, 0),),method
			)

	def reconnect(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def rename(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (24, 0), ((8, 0),),name
			)

	def renameBranch(self, index=defaultNamedNotOptArg, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (24, 0), ((3, 0), (8, 0)),index
			, name)

	def run(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def setBranchCondition(self, index=defaultNamedNotOptArg, condition=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1005, LCID, 1, (24, 0), ((3, 0), (8, 0)),index
			, condition)

	def show(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"AssociatedFiles": (15, 2, (12, 0), (), "AssociatedFiles", None),
		"Groups": (6, 2, (12, 0), (), "Groups", None),
		"IndexInParent": (18, 2, (3, 0), (), "IndexInParent", None),
		"ParentAssembly": (19, 2, (9, 0), (), "ParentAssembly", None),
		"Variables": (5, 2, (12, 0), (), "Variables", None),
		"exclusive": (1001, 2, (11, 0), (), "exclusive", None),
		"runLastBranchByDefault": (1002, 2, (11, 0), (), "runLastBranchByDefault", None),
		"userData": (11, 2, (12, 0), (), "userData", None),
	}
	_prop_map_put_ = {
		"AssociatedFiles" : ((15, LCID, 4, 0),()),
		"Groups" : ((6, LCID, 4, 0),()),
		"IndexInParent" : ((18, LCID, 4, 0),()),
		"ParentAssembly" : ((19, LCID, 4, 0),()),
		"Variables" : ((5, LCID, 4, 0),()),
		"exclusive" : ((1001, LCID, 4, 0),()),
		"runLastBranchByDefault" : ((1002, LCID, 4, 0),()),
		"userData" : ((11, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IIntegerArray(DispatchBaseClass):
	'Integer variable array'
	CLSID = IID('{6CBF1A44-679A-11D3-A518-00A024B5452E}')
	coclass_clsid = None

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (3, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	def clearLowerBound(self):
		return self._oleobj_.InvokeTypes(2019, LCID, 1, (24, 0), (),)

	def clearUpperBound(self):
		return self._oleobj_.InvokeTypes(2018, LCID, 1, (24, 0), (),)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFormattedStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2016, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getArray(self):
		return self._ApplyTypes_(2012, 1, (12, 0), (), 'getArray', None,)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getValue(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2010, LCID, 1, (3, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def getValueAbsolute(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2020, LCID, 1, (3, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def hasLowerBound(self):
		return self._oleobj_.InvokeTypes(2008, LCID, 1, (11, 0), (),)

	def hasUpperBound(self):
		return self._oleobj_.InvokeTypes(2009, LCID, 1, (11, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setArray(self, array=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2013, LCID, 1, (24, 0), ((12, 0),),array
			)

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setValue(self, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2011, LCID, 1, (24, 0), ((3, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),value
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def toFormattedStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2017, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toFormattedStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2015, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (3, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (2004, 2, (8, 0), (), "description", None),
		"enumAliases": (2006, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (2007, 2, (8, 0), (), "enumValues", None),
		"format": (2014, 2, (8, 0), (), "format", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"lowerBound": (2002, 2, (3, 0), (), "lowerBound", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
		"units": (2005, 2, (8, 0), (), "units", None),
		"upperBound": (2003, 2, (3, 0), (), "upperBound", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((2004, LCID, 4, 0),()),
		"enumAliases" : ((2006, LCID, 4, 0),()),
		"enumValues" : ((2007, LCID, 4, 0),()),
		"format" : ((2014, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"lowerBound" : ((2002, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
		"units" : ((2005, LCID, 4, 0),()),
		"upperBound" : ((2003, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (3, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IIntegerVariable(DispatchBaseClass):
	'Integer variable'
	CLSID = IID('{985910ED-C34D-11D2-A4E8-00A024B5452E}')
	coclass_clsid = None

	def clearLowerBound(self):
		return self._oleobj_.InvokeTypes(1016, LCID, 1, (24, 0), (),)

	def clearUpperBound(self):
		return self._oleobj_.InvokeTypes(1015, LCID, 1, (24, 0), (),)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFormattedString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1013, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def hasLowerBound(self):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (11, 0), (),)

	def hasUpperBound(self):
		return self._oleobj_.InvokeTypes(1010, LCID, 1, (11, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setInitialValue(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0),),value
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toFormattedString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1012, LCID, 1, (8, 0), (),)

	def toFormattedStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1014, LCID, 1, (8, 0), (),)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1005, 2, (8, 0), (), "description", None),
		"enumAliases": (1007, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (1006, 2, (8, 0), (), "enumValues", None),
		"format": (1011, 2, (8, 0), (), "format", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"lowerBound": (1002, 2, (3, 0), (), "lowerBound", None),
		"units": (1004, 2, (8, 0), (), "units", None),
		"upperBound": (1003, 2, (3, 0), (), "upperBound", None),
		"value": (1001, 2, (3, 0), (), "value", None),
		"valueAbsolute": (1017, 2, (3, 0), (), "valueAbsolute", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1005, LCID, 4, 0),()),
		"enumAliases" : ((1007, LCID, 4, 0),()),
		"enumValues" : ((1006, LCID, 4, 0),()),
		"format" : ((1011, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"lowerBound" : ((1002, LCID, 4, 0),()),
		"units" : ((1004, LCID, 4, 0),()),
		"upperBound" : ((1003, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
		"valueAbsolute" : ((1017, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (3, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IJobManager(DispatchBaseClass):
	'Job Manager object'
	CLSID = IID('{0C0D84B7-8376-4A71-AD4F-862AAD1BCE51}')
	coclass_clsid = None

	def addInput(self, name=defaultNamedNotOptArg, label=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((8, 0), (8, 0)),name
			, label)

	def addOutput(self, name=defaultNamedNotOptArg, label=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((8, 0), (8, 0)),name
			, label)

	def addRerun(self, run=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), ((3, 0),),run
			)

	def clearCache(self):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), (),)

	def enableCache(self, enable=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((11, 0),),enable
			)

	def getInput(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(14, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getInputLabel(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getNumInputs(self):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), (),)

	def getNumOutputs(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), (),)

	def getNumRuns(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), (),)

	def getNumThreads(self):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (3, 0), (),)

	def getOutput(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(15, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getOutputLabel(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getRunInParallel(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def getRunIndex(self, names=defaultNamedNotOptArg, values=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((12, 0), (12, 0)),names
			, values)

	def getValidateAll(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

	def halt(self, halt=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), ((11, 0),),halt
			)

	def resume(self, dataHistory=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((9, 0),),dataHistory
			)

	def setCustomMetadata(self, name=defaultNamedNotOptArg, key=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0)),name
			, key, value)

	def setInput(self, run=defaultNamedNotOptArg, name=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((3, 0), (8, 0), (8, 0)),run
			, name, value)

	def setNumRuns(self, numRuns=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((3, 0),),numRuns
			)

	def setNumThreads(self, numThreads=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((3, 0),),numThreads
			)

	def setRunInParallel(self, runInParallel=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((11, 0),),runInParallel
			)

	def setValidateAll(self, flag=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((11, 0),),flag
			)

	def submit(self, dataCollector=defaultNamedNotOptArg, description=defaultNamedOptArg, fireAndForget=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((9, 0), (12, 16), (12, 16)),dataCollector
			, description, fireAndForget)

	def waitForJobCompletion(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"wasHalted": (28, 2, (11, 0), (), "wasHalted", None),
	}
	_prop_map_put_ = {
		"wasHalted" : ((28, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ILogger(DispatchBaseClass):
	'Logger'
	CLSID = IID('{B478A93F-8BAC-43C5-9C4C-BD4AF8C9BAC1}')
	coclass_clsid = None

	def debug(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((8, 0),),message
			)

	def error(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),message
			)

	def info(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((8, 0),),message
			)

	def isDebugEnabled(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def isErrorEnabled(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

	def isInfoEnabled(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), (),)

	def isTraceEnabled(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (11, 0), (),)

	def isWarnEnabled(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), (),)

	def trace(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), ((8, 0),),message
			)

	def warn(self, message=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((8, 0),),message
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ILoginCallback(DispatchBaseClass):
	'Dispatch interface for ILoginCallback'
	CLSID = IID('{3C596B3E-0B8A-4B07-87D5-E9C165F858FB}')
	coclass_clsid = None

	def loginSucceeded(self, uri=defaultNamedNotOptArg, userName=defaultNamedNotOptArg, password=defaultNamedNotOptArg, savePassword=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0), (11, 0)),uri
			, userName, password, savePassword)

	def requestAuthCredentials(self, uri=defaultNamedNotOptArg, isFailedAttempt=defaultNamedNotOptArg, userName=defaultNamedNotOptArg, password=defaultNamedNotOptArg
			, savePassword=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((8, 0), (11, 0), (16396, 0), (16396, 0), (16396, 0)),uri
			, isFailedAttempt, userName, password, savePassword)

	def verifySslWarning(self, msg=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((8, 0),),msg
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IModelCenter(DispatchBaseClass):
	'ModelCenter main object'
	CLSID = IID('{BAACE1AA-EFDC-11D1-A4AD-00A024B5452E}')
	coclass_clsid = IID('{BAACE1AB-EFDC-11D1-A4AD-00A024B5452E}')

	def HTMLViewerGetMyHWND(self):
		return self._oleobj_.InvokeTypes(64, LCID, 1, (3, 0), (),)

	def HTMLViewerWaitForClose(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(63, LCID, 1, (24, 0), ((3, 0),),hwnd
			)

	def MessageBox(self, msg=defaultNamedNotOptArg, force=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), ((8, 0), (12, 16)),msg
			, force)

	def addIcon(self, iconFile=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(51, LCID, 1, (2, 0), ((8, 0),),iconFile
			)

	def addNewMacro(self, macroName=defaultNamedNotOptArg, isAppMacro=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(93, LCID, 1, (24, 0), ((8, 0), (11, 0)),macroName
			, isAppMacro)

	def autoLink(self, srcComp=defaultNamedNotOptArg, destComp=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(35, LCID, 1, (24, 0), ((8, 0), (8, 0)),srcComp
			, destComp)

	def breakLink(self, variable=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), ((8, 0),),variable
			)

	def checkout(self, feature=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((8, 0),),feature
			)
		if ret is not None:
			ret = Dispatch(ret, 'checkout', None)
		return ret

	def checkout2(self, feature=defaultNamedNotOptArg, productRelease=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(40, LCID, 1, (9, 0), ((8, 0), (8, 0)),feature
			, productRelease)
		if ret is not None:
			ret = Dispatch(ret, 'checkout2', None)
		return ret

	def closeHTMLViewer(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(62, LCID, 1, (11, 0), ((3, 0),),hwnd
			)

	def closeModel(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def configureLogging(self, enableLogging=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(78, LCID, 1, (24, 0), ((11, 0),),enableLogging
			)

	def createAndInitComponent(self, serverPath=defaultNamedNotOptArg, name=defaultNamedNotOptArg, parent=defaultNamedNotOptArg, initString=defaultNamedNotOptArg
			, xPos=defaultNamedOptArg, yPos=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(86, LCID, 1, (9, 0), ((8, 0), (8, 0), (8, 0), (8, 0), (12, 16), (12, 16)),serverPath
			, name, parent, initString, xPos, yPos
			)
		if ret is not None:
			ret = Dispatch(ret, 'createAndInitComponent', None)
		return ret

	def createAssembly(self, name=defaultNamedNotOptArg, parent=defaultNamedNotOptArg, AssemblyType=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(32, LCID, 1, (9, 0), ((8, 0), (8, 0), (12, 16)),name
			, parent, AssemblyType)
		if ret is not None:
			ret = Dispatch(ret, 'createAssembly', None)
		return ret

	def createAssemblyVariable(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, parent=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(33, LCID, 1, (9, 0), ((8, 0), (8, 0), (8, 0)),name
			, type, parent)
		if ret is not None:
			ret = Dispatch(ret, 'createAssemblyVariable', None)
		return ret

	def createComponent(self, serverPath=defaultNamedNotOptArg, name=defaultNamedNotOptArg, parent=defaultNamedNotOptArg, xPos=defaultNamedOptArg
			, yPos=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0), (12, 16), (12, 16)),serverPath
			, name, parent, xPos, yPos)

	def createDataCollector(self, tradeStudyType=defaultNamedNotOptArg, setup=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((8, 0), (8, 0)),tradeStudyType
			, setup)
		if ret is not None:
			ret = Dispatch(ret, 'createDataCollector', None)
		return ret

	def createDataExplorer(self, tradeStudyType=defaultNamedNotOptArg, setup=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(113, LCID, 1, (9, 0), ((8, 0), (8, 0)),tradeStudyType
			, setup)
		if ret is not None:
			ret = Dispatch(ret, 'createDataExplorer', None)
		return ret

	def createDataHistoryVariable(self):
		ret = self._oleobj_.InvokeTypes(110, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'createDataHistoryVariable', None)
		return ret

	def createDataMonitor(self, component=defaultNamedNotOptArg, name=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(49, LCID, 1, (9, 0), ((8, 0), (8, 0), (3, 0), (3, 0)),component
			, name, x, y)
		if ret is not None:
			ret = Dispatch(ret, 'createDataMonitor', None)
		return ret

	def createJobManager(self, showProgressDialog=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(19, LCID, 1, (9, 0), ((12, 16),),showProgressDialog
			)
		if ret is not None:
			ret = Dispatch(ret, 'createJobManager', None)
		return ret

	def createLink(self, variable=defaultNamedNotOptArg, equation=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((8, 0), (8, 0)),variable
			, equation)

	def createPlugInFrame(self, name=defaultNamedNotOptArg, title=defaultNamedNotOptArg, reserved=defaultNamedNotOptArg, plugIn=defaultNamedNotOptArg
			, showFavorites=defaultNamedOptArg, defaultHeight=defaultNamedOptArg, defaultWidth=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(42, LCID, 1, (3, 0), ((8, 0), (8, 0), (8, 0), (9, 0), (12, 16), (12, 16), (12, 16)),name
			, title, reserved, plugIn, showFavorites, defaultHeight
			, defaultWidth)

	def createPlugInFrame2(self, name=defaultNamedNotOptArg, title=defaultNamedNotOptArg, reserved=defaultNamedNotOptArg, plugIn=defaultNamedNotOptArg
			, showFavorites=defaultNamedOptArg, defaultHeight=defaultNamedOptArg, defaultWidth=defaultNamedOptArg, minimumHeight=defaultNamedOptArg, minimumWidth=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(77, LCID, 1, (3, 0), ((8, 0), (8, 0), (8, 0), (9, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),name
			, title, reserved, plugIn, showFavorites, defaultHeight
			, defaultWidth, minimumHeight, minimumWidth)

	def createTradeStudy(self, type=defaultNamedNotOptArg, setup=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(100, LCID, 1, (9, 0), ((8, 0), (12, 16)),type
			, setup)
		if ret is not None:
			ret = Dispatch(ret, 'createTradeStudy', None)
		return ret

	def destroyPlugInFrame(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(53, LCID, 1, (24, 0), ((3, 0),),hwnd
			)

	def displayAboutBox(self):
		return self._oleobj_.InvokeTypes(44, LCID, 1, (24, 0), (),)

	def displayPreferencesDialog(self):
		return self._oleobj_.InvokeTypes(46, LCID, 1, (24, 0), (),)

	def dumpComDebug(self):
		return self._oleobj_.InvokeTypes(107, LCID, 1, (24, 0), (),)

	def exit(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (24, 0), (),)

	def getActiveJobManager(self):
		ret = self._oleobj_.InvokeTypes(66, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getActiveJobManager', None)
		return ret

	def getAssembly(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(85, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getAssembly', None)
		return ret

	def getAssemblyStyle(self, assemblyName=defaultNamedNotOptArg, width=defaultNamedNotOptArg, height=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(84, LCID, 1, (3, 0), ((8, 0), (16387, 0), (16387, 0)),assemblyName
			, width, height)

	def getComponent(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getComponent', None)
		return ret

	def getDataCollector(self, index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(73, LCID, 1, (9, 0), ((3, 0),),index
			)
		if ret is not None:
			ret = Dispatch(ret, 'getDataCollector', None)
		return ret

	def getDataCollectorForDataExplorer(self, dataExplorer=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(118, LCID, 1, (9, 0), ((9, 0),),dataExplorer
			)
		if ret is not None:
			ret = Dispatch(ret, 'getDataCollectorForDataExplorer', None)
		return ret

	def getDataExplorer(self, index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(71, LCID, 1, (9, 0), ((3, 0),),index
			)
		if ret is not None:
			ret = Dispatch(ret, 'getDataExplorer', None)
		return ret

	def getDataMonitor(self, component=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(48, LCID, 1, (9, 0), ((8, 0), (12, 0)),component
			, index)
		if ret is not None:
			ret = Dispatch(ret, 'getDataMonitor', None)
		return ret

	def getFileSystemInfo(self, url=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(114, LCID, 1, (9, 0), ((8, 0),),url
			)
		if ret is not None:
			ret = Dispatch(ret, 'getFileSystemInfo', None)
		return ret

	def getFormatter(self, format=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(38, LCID, 1, (9, 0), ((8, 0),),format
			)
		if ret is not None:
			ret = Dispatch(ret, 'getFormatter', None)
		return ret

	def getGlobalParameters(self):
		ret = self._oleobj_.InvokeTypes(61, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getGlobalParameters', None)
		return ret

	def getHWND(self):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (3, 0), (),)

	def getHaltStatus(self):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), (),)

	def getLastErrorMessage(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (),)

	def getLicensingPath(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(87, LCID, 1, (8, 0), (),)

	def getLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(36, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'getLinks', None)
		return ret

	def getLogger(self):
		ret = self._oleobj_.InvokeTypes(75, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getLogger', None)
		return ret

	def getMacroScript(self, macroName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(89, LCID, 1, (8, 0), ((8, 0),),macroName
			)

	def getMacroScriptLanguage(self, macroName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(91, LCID, 1, (8, 0), ((8, 0),),macroName
			)

	def getMacroTimeout(self, macroName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(122, LCID, 1, (5, 0), ((8, 0),),macroName
			)

	def getModel(self):
		ret = self._oleobj_.InvokeTypes(22, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getModel', None)
		return ret

	def getModelCenterPath(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(69, LCID, 1, (8, 0), (),)

	def getModelUUID(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(37, LCID, 1, (8, 0), (),)

	def getNetworkLocations(self):
		ret = self._oleobj_.InvokeTypes(103, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'getNetworkLocations', None)
		return ret

	def getNumUnitCategories(self):
		return self._oleobj_.InvokeTypes(96, LCID, 1, (3, 0), (),)

	def getNumUnits(self, category=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(98, LCID, 1, (3, 0), ((8, 0),),category
			)

	def getPreference(self, pref=defaultNamedNotOptArg):
		return self._ApplyTypes_(67, 1, (12, 0), ((8, 0),), 'getPreference', None,pref
			)

	def getRunOnlyMode(self):
		return self._oleobj_.InvokeTypes(111, LCID, 1, (11, 0), (),)

	def getTradeStudyFilters(self):
		return self._ApplyTypes_(116, 1, (8200, 0), (), 'getTradeStudyFilters', None,)

	def getUnitCategoryName(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(97, LCID, 1, (8, 0), ((3, 0),),index
			)

	def getUnitName(self, category=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(99, LCID, 1, (8, 0), ((8, 0), (3, 0)),category
			, index)

	def getValue(self, varName=defaultNamedNotOptArg):
		return self._ApplyTypes_(4, 1, (12, 0), ((8, 0),), 'getValue', None,varName
			)

	def getValueAbsolute(self, varName=defaultNamedNotOptArg):
		return self._ApplyTypes_(24, 1, (12, 0), ((8, 0),), 'getValueAbsolute', None,varName
			)

	def getVariable(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariable', None)
		return ret

	def getVariableMetaData(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(106, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariableMetaData', None)
		return ret

	def getXMLExtension(self, nodeName=defaultNamedNotOptArg, attributeName=defaultNamedNotOptArg, attributeValue=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(81, LCID, 1, (8, 0), ((8, 0), (8, 0), (8, 0)),nodeName
			, attributeName, attributeValue)

	def guiCloseAllMultiplexers(self):
		return self._oleobj_.InvokeTypes(124, LCID, 1, (11, 0), (),)

	def guiLoadFile(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(120, LCID, 1, (11, 0), ((8, 0),),fileName
			)

	def guiSaveModel(self):
		return self._oleobj_.InvokeTypes(121, LCID, 1, (24, 0), (),)

	def halt(self):
		return self._oleobj_.InvokeTypes(45, LCID, 1, (24, 0), (),)

	def hidePlugInFrame(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(55, LCID, 1, (24, 0), ((3, 0),),hwnd
			)

	def internalLicensing(self, _MIDL__IModelCenter0000_=defaultNamedNotOptArg, _MIDL__IModelCenter0001_=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(68, LCID, 1, (24, 0), ((8, 0), (3, 0)),_MIDL__IModelCenter0000_
			, _MIDL__IModelCenter0001_)

	def invokeHelp(self, pageID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(39, LCID, 1, (24, 0), ((3, 0),),pageID
			)

	def isOkToClose(self):
		return self._oleobj_.InvokeTypes(50, LCID, 1, (11, 0), (),)

	def launchDataCollectorPlugIn(self, plugInName=defaultNamedNotOptArg, dataExplorer=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(119, LCID, 1, (24, 0), ((8, 0), (9, 0)),plugInName
			, dataExplorer)

	def launchHTMLViewer(self, url=defaultNamedNotOptArg, popup=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(59, LCID, 1, (3, 0), ((8, 0), (11, 0)),url
			, popup)

	def launchMacroEditor(self, macroName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(94, LCID, 1, (24, 0), ((8, 0),),macroName
			)

	def launchTradeStudy(self, type=defaultNamedNotOptArg, setup=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(41, LCID, 1, (24, 0), ((8, 0), (12, 16)),type
			, setup)

	def loadFile(self, fileName=defaultNamedNotOptArg, onConnectError=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((8, 0), (12, 16)),fileName
			, onConnectError)

	def loadModel(self, fileName=defaultNamedNotOptArg, onConnectError=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), ((8, 0), (12, 16)),fileName
			, onConnectError)

	def moveComponent(self, component=defaultNamedNotOptArg, parent=defaultNamedNotOptArg, index=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(79, LCID, 1, (24, 0), ((8, 0), (8, 0), (12, 16)),component
			, parent, index)

	def newModel(self, modelType=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((12, 16),),modelType
			)

	def parallelInstance(self):
		ret = self._oleobj_.InvokeTypes(74, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'parallelInstance', None)
		return ret

	def removeComponent(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((8, 0),),name
			)

	def removeDataMonitor(self, component=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(52, LCID, 1, (11, 0), ((8, 0), (12, 0)),component
			, index)

	def run(self, variableArray=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(47, LCID, 1, (24, 0), ((8, 0),),variableArray
			)

	def runAntFile(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(60, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def runMacro(self, macro=defaultNamedNotOptArg, useMCObject=defaultNamedOptArg):
		return self._ApplyTypes_(31, 1, (12, 0), ((8, 0), (12, 16)), 'runMacro', None,macro
			, useMCObject)

	def saveModel(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def saveModelAs(self, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), ((8, 0),),fileName
			)

	def saveTradeStudy(self, uri=defaultNamedNotOptArg, format=defaultNamedNotOptArg, dataExplorer=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(117, LCID, 1, (24, 0), ((8, 0), (3, 0), (9, 0)),uri
			, format, dataExplorer)

	def saveVersionedModel(self, VersionStatus=defaultNamedNotOptArg, checkinMessage=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(104, LCID, 1, (24, 0), ((3, 0), (8, 0)),VersionStatus
			, checkinMessage)

	def saveVersionedModelAs(self, fileName=defaultNamedNotOptArg, VersionStatus=defaultNamedNotOptArg, checkinMessage=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(105, LCID, 1, (24, 0), ((8, 0), (3, 0), (8, 0)),fileName
			, VersionStatus, checkinMessage)

	def setAlternateParentFrame(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 1, (24, 0), ((3, 0),),hwnd
			)

	def setAssemblyStyle(self, assemblyName=defaultNamedNotOptArg, style=defaultNamedNotOptArg, width=defaultNamedOptArg, height=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(83, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 16), (12, 16)),assemblyName
			, style, width, height)

	def setIconPlugInFrame(self, hwnd=defaultNamedNotOptArg, iconFile=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(56, LCID, 1, (24, 0), ((3, 0), (8, 0)),hwnd
			, iconFile)

	def setLoginCallback(self, callback=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(109, LCID, 1, (24, 0), ((9, 0),),callback
			)

	def setMacroScript(self, macroName=defaultNamedNotOptArg, script=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(90, LCID, 1, (24, 0), ((8, 0), (8, 0)),macroName
			, script)

	def setMacroScriptLanguage(self, macroName=defaultNamedNotOptArg, language=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(92, LCID, 1, (24, 0), ((8, 0), (8, 0)),macroName
			, language)

	def setMacroTimeout(self, macroName=defaultNamedNotOptArg, timeout=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(123, LCID, 1, (24, 0), ((8, 0), (5, 0)),macroName
			, timeout)

	def setPassword(self, password=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(58, LCID, 1, (24, 0), ((8, 0),),password
			)

	def setPreference(self, pref=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(101, LCID, 1, (24, 0), ((8, 0), (8, 0)),pref
			, value)

	def setRunOnlyMode(self, shouldBeInRunOnly=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(112, LCID, 1, (24, 0), ((11, 0),),shouldBeInRunOnly
			)

	def setScheduler(self, scheduler=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (24, 0), ((8, 0),),scheduler
			)

	def setUserName(self, userName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(57, LCID, 1, (24, 0), ((8, 0),),userName
			)

	def setValue(self, varName=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((8, 0), (8, 0)),varName
			, value)

	def setXMLExtension(self, xml=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(80, LCID, 1, (24, 0), ((8, 0),),xml
			)

	def showFileBrowseDialog(self, title=defaultNamedNotOptArg, filters=defaultNamedOptArg, initialUri=defaultNamedOptArg, hwnd=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(108, LCID, 1, (8, 0), ((8, 0), (12, 16), (12, 16), (12, 16)),title
			, filters, initialUri, hwnd)

	def showFileSaveDialog(self, title=defaultNamedNotOptArg, selectedFilter=defaultNamedNotOptArg, initialFilename=defaultNamedOptArg, filters=defaultNamedOptArg
			, initialUri=defaultNamedOptArg, hwnd=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(115, LCID, 1, (8, 0), ((8, 0), (16387, 0), (12, 16), (12, 16), (12, 16), (12, 16)),title
			, selectedFilter, initialFilename, filters, initialUri, hwnd
			)

	def showPlugInFrame(self, hwnd=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(54, LCID, 1, (24, 0), ((3, 0),),hwnd
			)

	def startGUIMode(self, showDialogs=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(95, LCID, 1, (24, 0), ((12, 16),),showDialogs
			)

	def tradeStudyEnd(self):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), (),)

	def tradeStudyStart(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	def transformAVPoint(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, screen=defaultNamedNotOptArg, tx=defaultNamedNotOptArg
			, ty=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(70, LCID, 1, (24, 0), ((3, 0), (3, 0), (11, 0), (16396, 0), (16396, 0)),x
			, y, screen, tx, ty)

	def unAssociatedInstance(self):
		ret = self._oleobj_.InvokeTypes(76, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'unAssociatedInstance', None)
		return ret

	# The method version is actually a property, but must be used as a method to correctly pass the arguments
	def version(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 2, (3, 0), ((3, 0),),index
			)

	_prop_map_get_ = {
		"IsInteractive": (82, 2, (3, 0), (), "IsInteractive", None),
		"ProcessID": (102, 2, (19, 0), (), "ProcessID", None),
		"appFullPath": (72, 2, (8, 0), (), "appFullPath", None),
		"appName": (65, 2, (8, 0), (), "appName", None),
		"modelDirectory": (15, 2, (8, 0), (), "modelDirectory", None),
		"modelFileName": (25, 2, (8, 0), (), "modelFileName", None),
		"screenUpdating": (18, 2, (11, 0), (), "screenUpdating", None),
	}
	_prop_map_put_ = {
		"IsInteractive" : ((82, LCID, 4, 0),()),
		"ProcessID" : ((102, LCID, 4, 0),()),
		"appFullPath" : ((72, LCID, 4, 0),()),
		"appName" : ((65, LCID, 4, 0),()),
		"modelDirectory" : ((15, LCID, 4, 0),()),
		"modelFileName" : ((25, LCID, 4, 0),()),
		"screenUpdating" : ((18, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class INetworkLocations(DispatchBaseClass):
	'Network Locations'
	CLSID = IID('{F036F767-ACF7-4128-823F-74E8B7E53EE9}')
	coclass_clsid = None

	def add(self, address=defaultNamedNotOptArg, userName=defaultNamedNotOptArg, password=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0)),address
			, userName, password)

	def exists(self, address=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((8, 0),),address
			)

	def removeAddress(self, address=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((8, 0),),address
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IObjectVariable(DispatchBaseClass):
	'Object variable'
	CLSID = IID('{989FF781-95F2-4CFA-A10E-57D169BDD0F3}')
	coclass_clsid = None

	def callMethod(self, method=defaultNamedNotOptArg):
		return self._ApplyTypes_(1018, 1, (12, 0), ((8, 0),), 'callMethod', None,method
			)

	def deleteAllMembers(self):
		return self._oleobj_.InvokeTypes(1017, LCID, 1, (24, 0), (),)

	def deleteMember(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1016, LCID, 1, (24, 0), ((8, 0),),member
			)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromFile(self, member=defaultNamedNotOptArg, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1050, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, fileName)

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromXML(self, str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1021, LCID, 1, (24, 0), ((8, 0),),str
			)

	def getArrayMember(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1105, 1, (12, 0), ((8, 0),), 'getArrayMember', None,member
			)

	def getArrayMemberAbsolute(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1104, 1, (12, 0), ((8, 0),), 'getArrayMemberAbsolute', None,member
			)

	def getArrayMemberValue(self, member=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._ApplyTypes_(1102, 1, (12, 0), ((8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)), 'getArrayMemberValue', None,member
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def getArrayMemberValueAbsolute(self, member=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._ApplyTypes_(1101, 1, (12, 0), ((8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)), 'getArrayMemberValueAbsolute', None,member
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def getClassURL(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1011, LCID, 1, (8, 0), (),)

	def getFileExtension(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1056, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getFileName(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1054, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getIsBinary(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1052, LCID, 1, (11, 0), ((8, 0),),member
			)

	def getMemberDescription(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1041, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getMemberDimensions(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1029, 1, (12, 0), ((8, 0),), 'getMemberDimensions', None,member
			)

	def getMemberEnumAliases(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1039, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getMemberEnumValues(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1037, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getMemberLength(self, member=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1025, LCID, 1, (3, 0), ((8, 0), (12, 16)),member
			, dim)

	def getMemberList(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1047, 1, (12, 0), ((8, 0),), 'getMemberList', None,member
			)

	def getMemberLowerBound(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1033, LCID, 1, (5, 0), ((8, 0),),member
			)

	def getMemberNumDimensions(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1028, LCID, 1, (3, 0), ((8, 0),),member
			)

	def getMemberProperty(self, member=defaultNamedNotOptArg, propertyName=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1045, LCID, 1, (8, 0), ((8, 0), (8, 0)),member
			, propertyName)

	def getMemberType(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1030, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getMemberUnits(self, member=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1043, LCID, 1, (8, 0), ((8, 0),),member
			)

	def getMemberUpperBound(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1035, LCID, 1, (5, 0), ((8, 0),),member
			)

	def getMemberValue(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1012, 1, (12, 0), ((8, 0),), 'getMemberValue', None,member
			)

	def getMemberValueAbsolute(self, member=defaultNamedNotOptArg):
		return self._ApplyTypes_(1013, 1, (12, 0), ((8, 0),), 'getMemberValueAbsolute', None,member
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getMethodList(self):
		return self._ApplyTypes_(1048, 1, (12, 0), (), 'getMethodList', None,)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def hasMember(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1022, LCID, 1, (11, 0), ((8, 0),),member
			)

	def hasMemberLowerBound(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1031, LCID, 1, (11, 0), ((8, 0),),member
			)

	def hasMemberUpperBound(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1032, LCID, 1, (11, 0), ((8, 0),),member
			)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isNonStrictType(self):
		return self._oleobj_.InvokeTypes(1019, LCID, 1, (11, 0), (),)

	def isNumericMember(self, member=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1023, LCID, 1, (11, 0), ((8, 0),),member
			)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def reinitialize(self):
		return self._oleobj_.InvokeTypes(1024, LCID, 1, (24, 0), (),)

	def setArrayMember(self, member=defaultNamedNotOptArg, array=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1106, LCID, 1, (24, 0), ((8, 0), (12, 0)),member
			, array)

	def setArrayMemberValue(self, member=defaultNamedNotOptArg, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg
			, d3=defaultNamedOptArg, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg
			, d8=defaultNamedOptArg, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1103, LCID, 1, (24, 0), ((8, 0), (8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),member
			, value, d1, d2, d3, d4
			, d5, d6, d7, d8, d9
			, d10)

	def setFileExtension(self, member=defaultNamedNotOptArg, fileExtension=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1057, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, fileExtension)

	def setFileName(self, member=defaultNamedNotOptArg, fileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1055, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, fileName)

	def setIsBinary(self, member=defaultNamedNotOptArg, isBinary=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1053, LCID, 1, (24, 0), ((8, 0), (11, 0)),member
			, isBinary)

	def setMember(self, member=defaultNamedNotOptArg, value=defaultNamedNotOptArg, type=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1015, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0)),member
			, value, type)

	def setMemberDescription(self, member=defaultNamedNotOptArg, description=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1042, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, description)

	def setMemberDimensions(self, member=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1027, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),member
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def setMemberEnumAliases(self, member=defaultNamedNotOptArg, enumAliases=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1040, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, enumAliases)

	def setMemberEnumValues(self, member=defaultNamedNotOptArg, enumValues=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1038, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, enumValues)

	def setMemberLength(self, member=defaultNamedNotOptArg, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1026, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 16)),member
			, length, dim)

	def setMemberLowerBound(self, member=defaultNamedNotOptArg, lowerBound=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1034, LCID, 1, (24, 0), ((8, 0), (5, 0)),member
			, lowerBound)

	def setMemberProperty(self, member=defaultNamedNotOptArg, propertyName=defaultNamedNotOptArg, propertyValue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1046, LCID, 1, (24, 0), ((8, 0), (8, 0), (8, 0)),member
			, propertyName, propertyValue)

	def setMemberUnits(self, member=defaultNamedNotOptArg, units=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1044, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, units)

	def setMemberUpperBound(self, member=defaultNamedNotOptArg, upperBound=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1036, LCID, 1, (24, 0), ((8, 0), (5, 0)),member
			, upperBound)

	def setMemberValue(self, member=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1014, LCID, 1, (24, 0), ((8, 0), (8, 0)),member
			, value)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toFile(self, member=defaultNamedNotOptArg, fileName=defaultNamedNotOptArg, encoding=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1049, LCID, 1, (24, 0), ((8, 0), (8, 0), (12, 0)),member
			, fileName, encoding)

	def toFileAbsolute(self, member=defaultNamedNotOptArg, fileName=defaultNamedNotOptArg, encoding=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1051, LCID, 1, (24, 0), ((8, 0), (8, 0), (12, 0)),member
			, fileName, encoding)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toXML(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1020, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1002, 2, (8, 0), (), "description", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"value": (1001, 2, (8, 0), (), "value", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1002, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (8, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IPHXFormat(DispatchBaseClass):
	CLSID = IID('{F7E774F5-A4CA-41D0-8F48-CC6B45043FB4}')
	coclass_clsid = None

	def doubleToEditableString(self, val=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), ((5, 0),),val
			)

	def doubleToString(self, val=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), ((5, 0),),val
			)

	def getFormat(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	def longToEditableString(self, val=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(8, LCID, 1, (8, 0), ((3, 0),),val
			)

	def longToString(self, val=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), ((3, 0),),val
			)

	def setFormat(self, format=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((8, 0),),format
			)

	def stringToDouble(self, str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (5, 0), ((8, 0),),str
			)

	def stringToLong(self, str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), ((8, 0),),str
			)

	def stringToString(self, str=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), ((8, 0),),str
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IRefArrayProp(DispatchBaseClass):
	'Reference variable array'
	CLSID = IID('{5BFF8381-7802-11D3-A524-00A024B5452E}')
	coclass_clsid = None

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	_prop_map_get_ = {
		"description": (4, 2, (8, 0), (), "description", None),
		"enumValues": (1, 2, (8, 0), (), "enumValues", None),
		"isInput": (2, 2, (11, 0), (), "isInput", None),
		"title": (3, 2, (8, 0), (), "title", None),
	}
	_prop_map_put_ = {
		"description" : ((4, LCID, 4, 0),()),
		"enumValues" : ((1, LCID, 4, 0),()),
		"isInput" : ((2, LCID, 4, 0),()),
		"title" : ((3, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IRefProp(DispatchBaseClass):
	'Reference property'
	CLSID = IID('{D3F8D5D4-7769-11D3-A522-00A024B5452E}')
	coclass_clsid = None

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	_prop_map_get_ = {
		"description": (4, 2, (8, 0), (), "description", None),
		"enumValues": (1, 2, (8, 0), (), "enumValues", None),
		"isInput": (2, 2, (11, 0), (), "isInput", None),
		"title": (3, 2, (8, 0), (), "title", None),
	}
	_prop_map_put_ = {
		"description" : ((4, LCID, 4, 0),()),
		"enumValues" : ((1, LCID, 4, 0),()),
		"isInput" : ((2, LCID, 4, 0),()),
		"title" : ((3, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IReferenceArray(DispatchBaseClass):
	'Reference variable array'
	CLSID = IID('{492AB501-6AA8-11D3-A519-00A024B5452E}')
	coclass_clsid = None

	# The method Setreference is actually a property, but must be used as a method to correctly pass the arguments
	def Setreference(self, index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2002, LCID, 4, (24, 0), ((3, 0), (8, 0)),index
			, arg1)

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((3, 0), (5, 0)),index
			, arg1)

	def createRefProp(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(2008, LCID, 1, (9, 0), ((8, 0), (8, 0)),name
			, type)
		if ret is not None:
			ret = Dispatch(ret, 'createRefProp', None)
		return ret

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getRefPropValue(self, name=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(2009, 1, (12, 0), ((8, 0), (3, 0)), 'getRefPropValue', None,name
			, index)

	def getRefPropValueAbsolute(self, name=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(2011, 1, (12, 0), ((8, 0), (3, 0)), 'getRefPropValueAbsolute', None,name
			, index)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getValue(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2004, LCID, 1, (5, 0), ((3, 0),),index
			)

	def getValueAbsolute(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2014, LCID, 1, (5, 0), ((3, 0),),index
			)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	# The method reference is actually a property, but must be used as a method to correctly pass the arguments
	def reference(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2002, LCID, 2, (8, 0), ((3, 0),),index
			)

	# The method referencedVariable is actually a property, but must be used as a method to correctly pass the arguments
	def referencedVariable(self, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(2013, 2, (12, 0), ((3, 0),), 'referencedVariable', None,index
			)

	# The method referencedVariables is actually a property, but must be used as a method to correctly pass the arguments
	def referencedVariables(self, index=defaultNamedNotOptArg):
		return self._ApplyTypes_(2012, 2, (12, 0), ((3, 0),), 'referencedVariables', None,index
			)

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setRefPropValue(self, name=defaultNamedNotOptArg, index=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2010, LCID, 1, (24, 0), ((8, 0), (3, 0), (8, 0)),name
			, index, value)

	def setValue(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2005, LCID, 1, (5, 0), ((5, 0), (3, 0)),value
			, index)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (5, 0), ((3, 0),),index
			)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"autoGrow": (2003, 2, (11, 0), (), "autoGrow", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"autoGrow" : ((2003, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (5, 0), ((3, 0),),index
			)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IReferenceVariable(DispatchBaseClass):
	'Reference variable'
	CLSID = IID('{4864FF03-3DE9-11D3-A50E-00A024B5452E}')
	coclass_clsid = None

	def createRefProp(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1005, LCID, 1, (9, 0), ((8, 0), (8, 0)),name
			, type)
		if ret is not None:
			ret = Dispatch(ret, 'createRefProp', None)
		return ret

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getRefPropValue(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(1006, 1, (12, 0), ((8, 0),), 'getRefPropValue', None,name
			)

	def getRefPropValueAbsolute(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(1008, 1, (12, 0), ((8, 0),), 'getRefPropValueAbsolute', None,name
			)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setRefPropValue(self, name=defaultNamedNotOptArg, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (24, 0), ((8, 0), (8, 0)),name
			, value)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"reference": (1002, 2, (8, 0), (), "reference", None),
		"referencedVariable": (1010, 2, (12, 0), (), "referencedVariable", None),
		"referencedVariables": (1009, 2, (12, 0), (), "referencedVariables", None),
		"value": (1001, 2, (5, 0), (), "value", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"reference" : ((1002, LCID, 4, 0),()),
		"referencedVariable" : ((1010, LCID, 4, 0),()),
		"referencedVariables" : ((1009, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (5, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IScriptComponent(DispatchBaseClass):
	'Script component'
	CLSID = IID('{126C0864-810E-535A-B648-F6F08C548BC3}')
	coclass_clsid = None

	def addVariable(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, state=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(1012, LCID, 1, (9, 0), ((8, 0), (8, 0), (8, 0)),name
			, type, state)
		if ret is not None:
			ret = Dispatch(ret, 'addVariable', None)
		return ret

	def downloadValues(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), (),)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (),)

	def getPositionX(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), (),)

	def getPositionY(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), (),)

	def getSource(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getSourceScript(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1015, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17, LCID, 1, (8, 0), (),)

	def getVariable(self, name=defaultNamedNotOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((8, 0),),name
			)
		if ret is not None:
			ret = Dispatch(ret, 'getVariable', None)
		return ret

	def invalidate(self):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), (),)

	def invokeMethod(self, method=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), ((8, 0),),method
			)

	def reconnect(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def removeVariable(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1013, LCID, 1, (24, 0), ((8, 0),),name
			)

	def rename(self, name=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (24, 0), ((8, 0),),name
			)

	def run(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def setSourceFromFile(self, file=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1011, LCID, 1, (24, 0), ((8, 0),),file
			)

	def setSourceFromString(self, script=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1010, LCID, 1, (24, 0), ((8, 0),),script
			)

	def setVariables(self, inputs=defaultNamedNotOptArg, outputs=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1014, LCID, 1, (24, 0), ((12, 0), (8, 0)),inputs
			, outputs)

	def show(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"AssociatedFiles": (15, 2, (12, 0), (), "AssociatedFiles", None),
		"Groups": (6, 2, (12, 0), (), "Groups", None),
		"IndexInParent": (18, 2, (3, 0), (), "IndexInParent", None),
		"ParentAssembly": (19, 2, (9, 0), (), "ParentAssembly", None),
		"Variables": (5, 2, (12, 0), (), "Variables", None),
		"forwardSchedule": (1003, 2, (11, 0), (), "forwardSchedule", None),
		"language": (1001, 2, (8, 0), (), "language", None),
		"prevalidate": (1004, 2, (11, 0), (), "prevalidate", None),
		"timeout": (1002, 2, (5, 0), (), "timeout", None),
		"userData": (11, 2, (12, 0), (), "userData", None),
	}
	_prop_map_put_ = {
		"AssociatedFiles" : ((15, LCID, 4, 0),()),
		"Groups" : ((6, LCID, 4, 0),()),
		"IndexInParent" : ((18, LCID, 4, 0),()),
		"ParentAssembly" : ((19, LCID, 4, 0),()),
		"Variables" : ((5, LCID, 4, 0),()),
		"forwardSchedule" : ((1003, LCID, 4, 0),()),
		"language" : ((1001, LCID, 4, 0),()),
		"prevalidate" : ((1004, LCID, 4, 0),()),
		"timeout" : ((1002, LCID, 4, 0),()),
		"userData" : ((11, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IShowHelpEvents:
	'Show Help events'
	CLSID = CLSID_Sink = IID('{F154331D-C65C-41A6-84D5-7BB9A065279D}')
	coclass_clsid = IID('{BAACE1AB-EFDC-11D1-A4AD-00A024B5452E}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnShowHelp",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnShowHelp(self, context=defaultNamedNotOptArg):


class IStringArray(DispatchBaseClass):
	'String variable array'
	CLSID = IID('{6CBF1A4C-679A-11D3-A518-00A024B5452E}')
	coclass_clsid = None

	# The method Setvalue is actually a property, but must be used as a method to correctly pass the arguments
	def Setvalue(self, d1=defaultNamedNotOptArg, d2=defaultNamedNotOptArg, d3=defaultNamedNotOptArg, d4=defaultNamedNotOptArg
			, d5=defaultNamedNotOptArg, d6=defaultNamedNotOptArg, d7=defaultNamedNotOptArg, d8=defaultNamedNotOptArg, d9=defaultNamedNotOptArg
			, d10=defaultNamedNotOptArg, arg10=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(2001, LCID, 4, (24, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (8, 0)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10, arg10
			)

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def fromStringEx(self, value=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1003, LCID, 1, (24, 0), ((8, 0), (3, 0)),value
			, index)

	def getArray(self):
		return self._ApplyTypes_(2007, 1, (12, 0), (), 'getArray', None,)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getLength(self, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1007, LCID, 1, (3, 0), ((12, 16),),dim
			)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def getValue(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2005, LCID, 1, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def getValueAbsolute(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2009, LCID, 1, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setArray(self, array=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2008, LCID, 1, (24, 0), ((12, 0),),array
			)

	def setDimensions(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1009, LCID, 1, (24, 0), ((3, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def setLength(self, length=defaultNamedNotOptArg, dim=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(1008, LCID, 1, (24, 0), ((3, 0), (12, 16)),length
			, dim)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def setValue(self, value=defaultNamedNotOptArg, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg
			, d4=defaultNamedOptArg, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg
			, d9=defaultNamedOptArg, d10=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(2006, LCID, 1, (24, 0), ((8, 0), (12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),value
			, d1, d2, d3, d4, d5
			, d6, d7, d8, d9, d10
			)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def toStringAbsoluteEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1004, LCID, 1, (8, 0), ((3, 0),),index
			)

	def toStringEx(self, index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(1002, LCID, 1, (8, 0), ((3, 0),),index
			)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	# The method value is actually a property, but must be used as a method to correctly pass the arguments
	def value(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (2002, 2, (8, 0), (), "description", None),
		"enumAliases": (2003, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (2004, 2, (8, 0), (), "enumValues", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"numDimensions": (1006, 2, (3, 0), (), "numDimensions", None),
		"size": (1001, 2, (3, 0), (), "size", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((2002, LCID, 4, 0),()),
		"enumAliases" : ((2003, LCID, 4, 0),()),
		"enumValues" : ((2004, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"numDimensions" : ((1006, LCID, 4, 0),()),
		"size" : ((1001, LCID, 4, 0),()),
	}
	# Default method for this class is 'value'
	def __call__(self, d1=defaultNamedNotOptArg, d2=defaultNamedOptArg, d3=defaultNamedOptArg, d4=defaultNamedOptArg
			, d5=defaultNamedOptArg, d6=defaultNamedOptArg, d7=defaultNamedOptArg, d8=defaultNamedOptArg, d9=defaultNamedOptArg
			, d10=defaultNamedOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(2001, LCID, 2, (8, 0), ((12, 0), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16), (12, 16)),d1
			, d2, d3, d4, d5, d6
			, d7, d8, d9, d10)

	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IStringVariable(DispatchBaseClass):
	'String variable'
	CLSID = IID('{985910E3-C34D-11D2-A4E8-00A024B5452E}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setInitialValue(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1005, LCID, 1, (24, 0), ((8, 0),),value
			)

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"description": (1002, 2, (8, 0), (), "description", None),
		"enumAliases": (1004, 2, (8, 0), (), "enumAliases", None),
		"enumValues": (1003, 2, (8, 0), (), "enumValues", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
		"value": (1001, 2, (8, 0), (), "value", None),
		"valueAbsolute": (1006, 2, (8, 0), (), "valueAbsolute", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"description" : ((1002, LCID, 4, 0),()),
		"enumAliases" : ((1004, LCID, 4, 0),()),
		"enumValues" : ((1003, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
		"value" : ((1001, LCID, 4, 0),()),
		"valueAbsolute" : ((1006, LCID, 4, 0),()),
	}
	# Default property for this class is 'value'
	def __call__(self):
		return self._ApplyTypes_(*(1001, 2, (8, 0), (), "value", None))
	def __str__(self, *args):
		return str(self.__call__(*args))
	def __int__(self, *args):
		return int(self.__call__(*args))
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ITradeStudyEvents:
	'Trade Study Run events'
	CLSID = CLSID_Sink = IID('{F2C901DF-0E2D-4715-9DE9-E69206ADF0C0}')
	coclass_clsid = IID('{BAACE1AB-EFDC-11D1-A4AD-00A024B5452E}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnStartToolRun",
		        2 : "OnEndToolRun",
		        3 : "OnToolClosed",
		        4 : "OnModelXMLExtensionsChanged",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnStartToolRun(self):
#	def OnEndToolRun(self):
#	def OnToolClosed(self, type=defaultNamedNotOptArg):
#	def OnModelXMLExtensionsChanged(self):


class IVariable(DispatchBaseClass):
	'Variable base class'
	CLSID = IID('{A0E042F1-B480-11D2-A4E6-00A024B5452E}')
	coclass_clsid = None

	def dependentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(14, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'dependentLinks', None)
		return ret

	def dependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'dependents', None)
		return ret

	def directDependents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directDependents', None)
		return ret

	def directPrecedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(11, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'directPrecedents', None)
		return ret

	def fromString(self, value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((8, 0),),value
			)

	def getFullName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (),)

	def getMetadata(self, name=defaultNamedNotOptArg):
		return self._ApplyTypes_(23, 1, (12, 0), ((8, 0),), 'getMetadata', None,name
			)

	def getName(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(3, LCID, 1, (8, 0), (),)

	def getType(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

	def invalidate(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

	def isInput(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), (),)

	def isInputToComponent(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), (),)

	def isInputToModel(self):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), (),)

	def isValid(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), (),)

	def precedentLinks(self, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), ((12, 16),),reserved
			)
		if ret is not None:
			ret = Dispatch(ret, 'precedentLinks', None)
		return ret

	def precedents(self, followSuspended=defaultNamedOptArg, reserved=defaultNamedOptArg):
		ret = self._oleobj_.InvokeTypes(15, LCID, 1, (9, 0), ((12, 16), (12, 16)),followSuspended
			, reserved)
		if ret is not None:
			ret = Dispatch(ret, 'precedents', None)
		return ret

	def setMetadata(self, name=defaultNamedNotOptArg, type=defaultNamedNotOptArg, value=defaultNamedNotOptArg, access=defaultNamedNotOptArg
			, archive=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), ((8, 0), (3, 0), (12, 0), (3, 0), (11, 0)),name
			, type, value, access, archive)

	def toString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(7, LCID, 1, (8, 0), (),)

	def toStringAbsolute(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(9, LCID, 1, (8, 0), (),)

	def validate(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"OwningComponent": (22, 2, (9, 0), (), "OwningComponent", None),
		"hasChanged": (17, 2, (11, 0), (), "hasChanged", None),
		"hide": (18, 2, (11, 0), (), "hide", None),
	}
	_prop_map_put_ = {
		"OwningComponent" : ((22, LCID, 4, 0),()),
		"hasChanged" : ((17, LCID, 4, 0),()),
		"hide" : ((18, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IVariableDescription(DispatchBaseClass):
	'Variable description'
	CLSID = IID('{EAE610F5-CC85-11D5-A008-0010A4C22C0F}')
	coclass_clsid = None

	_prop_map_get_ = {
		"equation": (6, 2, (8, 0), (), "equation", None),
		"fullName": (2, 2, (8, 0), (), "fullName", None),
		"isCustom": (5, 2, (11, 0), (), "isCustom", None),
		"isNumeric": (8, 2, (11, 0), (), "isNumeric", None),
		"name": (1, 2, (8, 0), (), "name", None),
		"state": (3, 2, (2, 0), (), "state", None),
		"type": (7, 2, (8, 0), (), "type", None),
		"units": (4, 2, (8, 0), (), "units", None),
	}
	_prop_map_put_ = {
		"equation" : ((6, LCID, 4, 0),()),
		"fullName" : ((2, LCID, 4, 0),()),
		"isCustom" : ((5, LCID, 4, 0),()),
		"isNumeric" : ((8, LCID, 4, 0),()),
		"name" : ((1, LCID, 4, 0),()),
		"state" : ((3, LCID, 4, 0),()),
		"type" : ((7, LCID, 4, 0),()),
		"units" : ((4, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IVariableLink(DispatchBaseClass):
	'VariableLink object'
	CLSID = IID('{0F11CB29-B367-40ED-8F26-BD4A54DACF2A}')
	coclass_clsid = None

	def breakLink(self):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	def resumeLink(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

	def suspendLink(self):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"LHS": (1, 2, (8, 0), (), "LHS", None),
		"RHS": (2, 2, (8, 0), (), "RHS", None),
	}
	_prop_map_put_ = {
		"LHS" : ((1, LCID, 4, 0),()),
		"RHS" : ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IVariableLinks(DispatchBaseClass):
	'VariableLinks collection'
	CLSID = IID('{C5B28059-9C9F-4EA3-9AB1-B9EDE06C4152}')
	coclass_clsid = None

	def Item(self, id=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (12, 0), ((12, 0),), 'Item', None,id
			)

	_prop_map_get_ = {
		"Count": (1, 2, (12, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 1, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (12, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IVariables(DispatchBaseClass):
	'Variables object'
	CLSID = IID('{CC3F2432-D179-4018-835F-34173613824B}')
	coclass_clsid = None

	def Item(self, id=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (12, 0), ((12, 0),), 'Item', None,id
			)

	_prop_map_get_ = {
		"Count": (1, 2, (12, 0), (), "Count", None),
	}
	_prop_map_put_ = {
		"Count" : ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Item property/method which allows indexed access with the object[key] syntax.
	#Some objects will accept a string or other type of key in addition to integers.
	#Note that many Office objects do not use zero-based indexing.
	def __getitem__(self, key):
		return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 1, 1, key)), "Item", None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(1, 2, (12, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IVizContainer(DispatchBaseClass):
	'VizContainer'
	CLSID = IID('{D57D1AA5-B852-4EB1-991E-7433AF3E0006}')
	coclass_clsid = None

	def fileSaved(self):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), (),)

	def hide(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

	def show(self):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	def showAt(self, top=defaultNamedNotOptArg, left=defaultNamedNotOptArg, width=defaultNamedNotOptArg, height=defaultNamedNotOptArg
			, state=defaultNamedOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((3, 0), (3, 0), (3, 0), (3, 0), (12, 16)),top
			, left, width, height, state)

	_prop_map_get_ = {
		"DataExplorerPlugIn": (3, 2, (9, 0), (), "DataExplorerPlugIn", None),
		"Visible": (1, 2, (11, 0), (), "Visible", None),
		"dataExplorer": (6, 2, (9, 0), (), "dataExplorer", None),
		"hwnd": (2, 2, (3, 0), (), "hwnd", None),
	}
	_prop_map_put_ = {
		"DataExplorerPlugIn" : ((3, LCID, 4, 0),()),
		"Visible" : ((1, LCID, 4, 0),()),
		"dataExplorer" : ((6, LCID, 4, 0),()),
		"hwnd" : ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'ModelCenter.Application'
class Application(CoClassBaseClass): # A CoClass
	CLSID = IID('{BAACE1AB-EFDC-11D1-A4AD-00A024B5452E}')
	coclass_sources = [
		ITradeStudyEvents,
		IShowHelpEvents,
	]
	default_source = ITradeStudyEvents
	coclass_interfaces = [
		IModelCenter,
	]
	default_interface = IModelCenter

RecordMap = {
}

CLSIDToClassMap = {
	'{6B3DCC47-6475-411C-977E-337F73A43771}' : IAddToModel,
	'{6CBF1A48-679A-11D3-A518-00A024B5452E}' : IArray,
	'{0D132C3C-CA70-11D5-A008-0010A4C22C0F}' : IAssemblies,
	'{0D132C36-CA70-11D5-A008-0010A4C22C0F}' : IAssembly,
	'{6CBF1A4F-679A-11D3-A518-00A024B5452E}' : IBooleanArray,
	'{985910EA-C34D-11D2-A4E8-00A024B5452E}' : IBooleanVariable,
	'{526AC1E1-D718-11D3-A544-00A024B5452E}' : IComponent,
	'{712469FD-A1E9-4450-BE93-457ED13A91F1}' : IComponents,
	'{897C0864-810E-444A-B648-F6F08C639BC3}' : IIfComponent,
	'{126C0864-810E-535A-B648-F6F08C548BC3}' : IScriptComponent,
	'{214FB734-840B-4BC1-A063-1D2DFA0C6D0A}' : ICustomDesignPoint,
	'{1539CF41-7B1A-11D3-A526-00A024B5452E}' : IDataCollector,
	'{514D1080-6A11-11D3-A518-00A024B5452E}' : IDoubleArray,
	'{985910E7-C34D-11D2-A4E8-00A024B5452E}' : IDoubleVariable,
	'{989FF781-95F2-4CFA-A10E-57D169BDD0F3}' : IObjectVariable,
	'{22D5CD66-AF6F-48F7-AC03-80095DE85C94}' : IFeature,
	'{14F18BD0-5BD9-4FCC-B084-7D95360631BE}' : IFileArray,
	'{A79BA2F2-C8C2-11D5-A008-0010A4C22C0F}' : IFileVariable,
	'{E45A67F4-C367-11D2-A4E8-00A024B5452E}' : IGeometryVariable,
	'{0D132C39-CA70-11D5-A008-0010A4C22C0F}' : IGroup,
	'{0D132C3F-CA70-11D5-A008-0010A4C22C0F}' : IGroups,
	'{6CBF1A44-679A-11D3-A518-00A024B5452E}' : IIntegerArray,
	'{985910ED-C34D-11D2-A4E8-00A024B5452E}' : IIntegerVariable,
	'{0C0D84B7-8376-4A71-AD4F-862AAD1BCE51}' : IJobManager,
	'{BAACE1AA-EFDC-11D1-A4AD-00A024B5452E}' : IModelCenter,
	'{3C596B3E-0B8A-4B07-87D5-E9C165F858FB}' : ILoginCallback,
	'{F2C901DF-0E2D-4715-9DE9-E69206ADF0C0}' : ITradeStudyEvents,
	'{F154331D-C65C-41A6-84D5-7BB9A065279D}' : IShowHelpEvents,
	'{BAACE1AB-EFDC-11D1-A4AD-00A024B5452E}' : Application,
	'{F036F767-ACF7-4128-823F-74E8B7E53EE9}' : INetworkLocations,
	'{5BFF8381-7802-11D3-A524-00A024B5452E}' : IRefArrayProp,
	'{492AB501-6AA8-11D3-A519-00A024B5452E}' : IReferenceArray,
	'{4864FF03-3DE9-11D3-A50E-00A024B5452E}' : IReferenceVariable,
	'{D3F8D5D4-7769-11D3-A522-00A024B5452E}' : IRefProp,
	'{6CBF1A4C-679A-11D3-A518-00A024B5452E}' : IStringArray,
	'{985910E3-C34D-11D2-A4E8-00A024B5452E}' : IStringVariable,
	'{A0E042F1-B480-11D2-A4E6-00A024B5452E}' : IVariable,
	'{EAE610F5-CC85-11D5-A008-0010A4C22C0F}' : IVariableDescription,
	'{0F11CB29-B367-40ED-8F26-BD4A54DACF2A}' : IVariableLink,
	'{C5B28059-9C9F-4EA3-9AB1-B9EDE06C4152}' : IVariableLinks,
	'{CC3F2432-D179-4018-835F-34173613824B}' : IVariables,
	'{F7E774F5-A4CA-41D0-8F48-CC6B45043FB4}' : IPHXFormat,
	'{B4009E4E-5E90-4B44-8687-143051AA7400}' : IDataMonitor,
	'{CBBF5B6F-ED70-463D-B1E6-6DAE10500A4E}' : IGlobalParameters,
	'{B478A93F-8BAC-43C5-9C4C-BD4AF8C9BAC1}' : ILogger,
	'{631F5771-6F41-495F-BF88-55368128C415}' : ICachePin,
	'{3E645325-85F9-456B-B5B7-395C90825986}' : IFileSystemInfo,
	'{D57D1AA5-B852-4EB1-991E-7433AF3E0006}' : IVizContainer,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'IAddToModel' : '{6B3DCC47-6475-411C-977E-337F73A43771}',
	'IArray' : '{6CBF1A48-679A-11D3-A518-00A024B5452E}',
	'IAssemblies' : '{0D132C3C-CA70-11D5-A008-0010A4C22C0F}',
	'IAssembly' : '{0D132C36-CA70-11D5-A008-0010A4C22C0F}',
	'IBooleanArray' : '{6CBF1A4F-679A-11D3-A518-00A024B5452E}',
	'IBooleanVariable' : '{985910EA-C34D-11D2-A4E8-00A024B5452E}',
	'IComponent' : '{526AC1E1-D718-11D3-A544-00A024B5452E}',
	'IComponents' : '{712469FD-A1E9-4450-BE93-457ED13A91F1}',
	'IIfComponent' : '{897C0864-810E-444A-B648-F6F08C639BC3}',
	'IScriptComponent' : '{126C0864-810E-535A-B648-F6F08C548BC3}',
	'ICustomDesignPoint' : '{214FB734-840B-4BC1-A063-1D2DFA0C6D0A}',
	'IDataCollector' : '{1539CF41-7B1A-11D3-A526-00A024B5452E}',
	'IDoubleArray' : '{514D1080-6A11-11D3-A518-00A024B5452E}',
	'IDoubleVariable' : '{985910E7-C34D-11D2-A4E8-00A024B5452E}',
	'IObjectVariable' : '{989FF781-95F2-4CFA-A10E-57D169BDD0F3}',
	'IFeature' : '{22D5CD66-AF6F-48F7-AC03-80095DE85C94}',
	'IFileArray' : '{14F18BD0-5BD9-4FCC-B084-7D95360631BE}',
	'IFileVariable' : '{A79BA2F2-C8C2-11D5-A008-0010A4C22C0F}',
	'IGeometryVariable' : '{E45A67F4-C367-11D2-A4E8-00A024B5452E}',
	'IGroup' : '{0D132C39-CA70-11D5-A008-0010A4C22C0F}',
	'IGroups' : '{0D132C3F-CA70-11D5-A008-0010A4C22C0F}',
	'IIntegerArray' : '{6CBF1A44-679A-11D3-A518-00A024B5452E}',
	'IIntegerVariable' : '{985910ED-C34D-11D2-A4E8-00A024B5452E}',
	'IJobManager' : '{0C0D84B7-8376-4A71-AD4F-862AAD1BCE51}',
	'IModelCenter' : '{BAACE1AA-EFDC-11D1-A4AD-00A024B5452E}',
	'ILoginCallback' : '{3C596B3E-0B8A-4B07-87D5-E9C165F858FB}',
	'ITradeStudyEvents' : '{F2C901DF-0E2D-4715-9DE9-E69206ADF0C0}',
	'IShowHelpEvents' : '{F154331D-C65C-41A6-84D5-7BB9A065279D}',
	'INetworkLocations' : '{F036F767-ACF7-4128-823F-74E8B7E53EE9}',
	'IRefArrayProp' : '{5BFF8381-7802-11D3-A524-00A024B5452E}',
	'IReferenceArray' : '{492AB501-6AA8-11D3-A519-00A024B5452E}',
	'IReferenceVariable' : '{4864FF03-3DE9-11D3-A50E-00A024B5452E}',
	'IRefProp' : '{D3F8D5D4-7769-11D3-A522-00A024B5452E}',
	'IStringArray' : '{6CBF1A4C-679A-11D3-A518-00A024B5452E}',
	'IStringVariable' : '{985910E3-C34D-11D2-A4E8-00A024B5452E}',
	'IVariable' : '{A0E042F1-B480-11D2-A4E6-00A024B5452E}',
	'IVariableDescription' : '{EAE610F5-CC85-11D5-A008-0010A4C22C0F}',
	'IVariableLink' : '{0F11CB29-B367-40ED-8F26-BD4A54DACF2A}',
	'IVariableLinks' : '{C5B28059-9C9F-4EA3-9AB1-B9EDE06C4152}',
	'IVariables' : '{CC3F2432-D179-4018-835F-34173613824B}',
	'IPHXFormat' : '{F7E774F5-A4CA-41D0-8F48-CC6B45043FB4}',
	'IDataMonitor' : '{B4009E4E-5E90-4B44-8687-143051AA7400}',
	'IGlobalParameters' : '{CBBF5B6F-ED70-463D-B1E6-6DAE10500A4E}',
	'ILogger' : '{B478A93F-8BAC-43C5-9C4C-BD4AF8C9BAC1}',
	'ICachePin' : '{631F5771-6F41-495F-BF88-55368128C415}',
	'IFileSystemInfo' : '{3E645325-85F9-456B-B5B7-395C90825986}',
	'IVizContainer' : '{D57D1AA5-B852-4EB1-991E-7433AF3E0006}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

