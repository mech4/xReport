import sys
import os
import com.ihsan.foundation.pobject as pobject

class DTS(pobject.PObject):
  # static variable
  pobject_classname = 'DTS' # AS DEFINED IN METADATA
  pobject_keys = ['DTSId'] # AS DEFINED IN METADATA
#--

class DTSFolder(pobject.PObject):
  # static variable
  pobject_classname = 'DTSFolder' # AS DEFINED IN METADATA
  pobject_keys = ['DTSFolderId'] # AS DEFINED IN METADATA
#--

class DTSFile(pobject.PObject):
  # static variable
  pobject_classname = 'DTSFile' # AS DEFINED IN METADATA
  pobject_keys = ['DTSFileId'] # AS DEFINED IN METADATA
#--

class DTSAlias(pobject.PObject):
  # static variable
  pobject_classname = 'DTSAlias' # AS DEFINED IN METADATA
  pobject_keys = ['DTSAliasId'] # AS DEFINED IN METADATA
#--

class DTSEnum(pobject.PObject):
  # static variable
  pobject_classname = 'DTSEnum' # AS DEFINED IN METADATA
  pobject_keys = ['DTSEnumName', 'DTSEnumValue'] # AS DEFINED IN METADATA
#--

class DTSForm(DTSFile):
  # static variable
  pobject_classname = 'DTSForm' # AS DEFINED IN METADATA
  pobject_keys = ['DTSFileId'] # AS DEFINED IN METADATA
#--

class DTSMap(pobject.PObject):
  # static variable
  pobject_classname = 'DTSMap' # AS DEFINED IN METADATA
  pobject_keys = ['DTSMapId'] # AS DEFINED IN METADATA
#--

class DTSMapQuery(pobject.PObject):
  # static variable
  pobject_classname = 'DTSMapQuery' # AS DEFINED IN METADATA
  pobject_keys = ['DTSMapQueryId'] # AS DEFINED IN METADATA
#--

class DTSReport(pobject.PObject):
  # static variable
  pobject_classname = 'DTSReport' # AS DEFINED IN METADATA
  pobject_keys = ['DTSReportId'] # AS DEFINED IN METADATA
#--

class DTSMeta(pobject.PObject):
  # static variable
  pobject_classname = 'DTSMeta' # AS DEFINED IN METADATA
  pobject_keys = ['DTSMetaId'] # AS DEFINED IN METADATA
#--