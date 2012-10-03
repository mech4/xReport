import sys
import os
import com.ihsan.foundation.pobject as pobject
import com.ihsan.util.attrutil as attrutil

class ReportClassGroup(pobject.PObject):
  # static variable
  pobject_classname = 'ReportClassGroup' # AS DEFINED IN METADATA
  pobject_keys = ['group_id'] # AS DEFINED IN METADATA
#--

class ReportClass(pobject.PObject):
  # static variable
  pobject_classname = 'ReportClass' # AS DEFINED IN METADATA
  pobject_keys = ['class_id'] # AS DEFINED IN METADATA
#--

class Report(pobject.PObject):
  # static variable
  pobject_classname = 'Report' # AS DEFINED IN METADATA
  pobject_keys = ['report_id'] # AS DEFINED IN METADATA
  
  def OnCreate(self, parameters):
    attrutil.transferAttributes(self.Helper, [
      "class_id=class_id", "period_id=period_id", "branch_id=branch_id"
    ], self, parameters)
  #--
#--

class Period(pobject.PObject):
  # static variable
  pobject_classname = 'Period' # AS DEFINED IN METADATA
  pobject_keys = ['period_id'] # AS DEFINED IN METADATA
#--

class Branch(pobject.PObject):
  # static variable
  pobject_classname = 'Branch' # AS DEFINED IN METADATA
  pobject_keys = ['branch_id'] # AS DEFINED IN METADATA  
#--

class BranchMember(pobject.PObject):
  # static variable
  pobject_classname = 'BranchMember' # AS DEFINED IN METADATA
  pobject_keys = ['member_id'] # AS DEFINED IN METADATA
#--

class ReportItem(pobject.PObject):
  # static variable
  pobject_classname = 'ReportItem' # AS DEFINED IN METADATA
  pobject_keys = ['item_id'] # AS DEFINED IN METADATA
#--

