# DEFS
ATTR_ORACLE   = 0x01
ATTR_MONGODB  = 0x02 
ATTR_TYPE     = ATTR_ORACLE  

class fGlobalReport:
  def __init__(self, formObj, parentForm):
    self.repform     = None
    self.group_code  = None
    self.period_type = None
  #--

  def setAttrList(self):
    if self.repform != None:
      reflist  = self.repform.reflist
      attrlist = [] 
      for refname in reflist:
        if ATTR_TYPE == ATTR_MONGODB:
          attrlist.append("{0}_refdata_id={0}.refdata_id".format(refname))
          attrlist.append("{0}_reference_code={0}.reference_code".format(refname))
          attrlist.append("{0}_reference_desc={0}.reference_desc".format(refname))
        elif ATTR_TYPE == ATTR_ORACLE:
          attrlist.append("{0}_refdata_id={0}.refdata_id".format(refname))
      #--               
      self.save_attrlist = attrlist + self.repform.attrlist
      
      attrlist = [] 
      for refname in reflist:
        if ATTR_TYPE == ATTR_MONGODB:
          attrlist.append("{0}.refdata_id={0}_refdata_id".format(refname))
          attrlist.append("{0}.reference_code={0}_reference_code".format(refname))
          attrlist.append("{0}.reference_desc={0}_reference_desc".format(refname))
        elif ATTR_TYPE == ATTR_ORACLE:
          attrlist.append("{0}.refdata_id={0}.refdata_id".format(refname))
          attrlist.append("{0}.reference_code={0}.reference_code".format(refname))
          attrlist.append("{0}.reference_desc={0}.reference_desc".format(refname))
      #--               
      self.load_attrlist = ['item_id'] + attrlist + self.repform.attrlist
    #--   
    
  def Show(self, group_code, period_type):
    self.group_code = group_code
    self.period_type = period_type
    ph = self.FormObject.ClientApplication.CreateValues(
         ['period_type', period_type]
    )
    res = self.FormObject.CallServerMethod('PeriodCheck', ph)
    self.FormContainer.Show()
    
  def branchOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("branch.branch_code") == "-":
      self.uipMain.ClearLink("branch")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupBranch", "branch", 
        "branch_code;branch_name;branch_id")
        
      return res

  def periodOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("period.period_code") == '-':
      self.uipMain.ClearLink("period")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupPeriod", "period", 
        "period_code;description;period_id", None, 
        {'period_type': self.period_type})
        
      return res

  def bGenerateOnClick(self, sender):
    formobj = self.FormObject; app = formobj.ClientApplication
    
    uipMain = self.uipMain
    ph = app.CreateValues(
      ['group_code', self.group_code]
      , ["period_id", uipMain.GetFieldValue("period.period_id")]
      , ["branch_id", uipMain.GetFieldValue("branch.branch_id")]
    )
    ph = formobj.CallServerMethod('GenerateTxt', ph)
    
    status = ph.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    else:
      oPrint = app.GetClientClass('PrintLib','PrintLib')()
      oPrint.doProcess(app, ph.packet, 1)    
    #--
    
  #--