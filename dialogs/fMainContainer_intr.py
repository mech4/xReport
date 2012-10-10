# DEFS
ATTR_ORACLE   = 0x01
ATTR_MONGODB  = 0x02 
ATTR_TYPE     = ATTR_ORACLE  

class fReportContainer:
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
    self.FormContainer.Show()
    self.switchEdit(False)
    
  def branchOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("branch.branch_code") == "-":
      self.uipMain.ClearLink("branch")
    else:  
      res = uapp.stdLookup(sender, "report@lookupBranch", "branch", 
        "branch_code;branch_name;branch_id")
        
      return res

  def periodOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("period.period_code") == '-':
      self.uipMain.ClearLink("period")
    else:  
      res = uapp.stdLookup(sender, "report@lookupPeriod", "period", 
        "period_code;description;period_id", None, 
        {'period_type': self.period_type})
        
      return res

  def reportOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("reportclass.report_code") == '-':
      self.uipMain.ClearLink("reportclass")
    else:  
      res = uapp.stdLookup(sender, "report@lookupReportClass", "reportclass", 
        "report_code;report_name;class_id;form_id", None, 
        {'group_code': self.group_code})
        
      return res

  def switchEdit(self, swOn=True):
    if self.repform != None:
      self.repform.pData.SetAllControlsReadOnly(not swOn)
    self.pData_bSave.enabled = swOn
    self.pData_bDownload.enabled = swOn
    self.pData_bGenerate.enabled = swOn
    self.pAction_bNewrow.enabled = swOn
    self.pAction_bDeleteRow.enabled = swOn
    
  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    formobj = self.FormObject; app = formobj.ClientApplication
    
    if self.repform == None: return
    self.uipMain.attrlist   = str(self.save_attrlist)
    self.uipMain.group_code = self.group_code
    
    formobj.CommitBuffer()
    self.repform.FormObject.CommitBuffer()
    
    ph = formobj.GetDataPacket()
    repph = self.repform.FormObject.GetDataPacket(1) 
    ph.Packet.AcquireAnotherPacket(repph.Packet)
    
    ph = formobj.CallServerMethod('SaveReport', ph)
    
    status = ph.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    else:
      app.ShowMessage('Data successfully save.')
      self.switchEdit(False)
    #--
    
  def bLoadOnClick(self, sender):
    # procedure(sender: TrtfButton)
    # procedure(sender: TrtfButton)
    formObj = self.FormObject; app = formObj.ClientApplication
    uipMain = self.uipMain
     
    formid = uipMain.GetFieldValue("reportclass.form_id") or ''
    if formid == '':
      app.ShowMessage("Input not completed yet!")
      return
           
    self.repform = self.frReport.Activate(formid, app.CreatePacket(), None)
    self.setAttrList()
    
    ph = app.CreateValues(
      ["class_id", uipMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uipMain.GetFieldValue("period.period_id")]
      , ["branch_id", uipMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uipMain.GetFieldValue("reportclass.report_code")]
      , ["attrlist", str(self.load_attrlist)]
    )
    self.repform.FormObject.SetDataWithParameters(ph)
    self.switchEdit()

  def bNewRowOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.repform != None:
      self.repform.uipData.Append()
      self.repform.pData.GetControl(0).SetFocus()
    #--

  def bDeleteRowOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.repform != None:
      item_id = self.repform.uipData.item_id or -1
      if item_id != -1:
        self.uipDeleted.Append()
        self.uipDeleted.item_id = item_id
        self.uipDeleted.Post()
      #--
      self.repform.uipData.Delete()
    #--

  def bSaveRowOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.repform != None:
      self.repform.uipData.Post()
    #--


  def bDownloadOnClick(self, sender):
    formobj = self.FormObject; app = formobj.ClientApplication
    
    uMain = self.uipMain    
    ph = app.CreateValues(
      ["class_id", uMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uMain.GetFieldValue("period.period_id")]
      , ["branch_id", uMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uMain.GetFieldValue("reportclass.report_code")]
      , ["xlstemplate", self.repform.xlstemplate]
      , ["xlstopline", str(self.repform.xlstopline)]
      , ["xlsmap", str(self.repform.xlsmap)]
      , ["reflist", str(self.repform.reflist)]
    )
    
    ph = formobj.CallServerMethod('DownloadReport', ph)
    
    status = ph.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    else:
      oPrint = app.GetClientClass('PrintLib','PrintLib')()
      oPrint.doProcess(app, ph.packet, 1)    
    #--
    

  def bGenerateOnClick(self, sender):
    formobj = self.FormObject; app = formobj.ClientApplication
    
    uMain = self.uipMain    
    ph = app.CreateValues(
      ["class_id", uMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uMain.GetFieldValue("period.period_id")]
      , ["branch_id", uMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uMain.GetFieldValue("reportclass.report_code")]
      , ["txttemplate", self.repform.txttemplate]
      , ["txtmap", str(self.repform.txtmap)]
      , ["xlsmap", str(self.repform.xlsmap)]
      , ["reflist", str(self.repform.reflist)]
      , ["useheader", str(self.repform.useheader)]
    )
    
    ph = formobj.CallServerMethod('GenerateTxt', ph)
    
    status = ph.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    else:
      oPrint = app.GetClientClass('PrintLib','PrintLib')()
      oPrint.doProcess(app, ph.packet, 1)    
    #--
    
