class fReportChecklist:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self):
    uip = self.uipart1
    #for auto
    #uip.SetFieldValue('lDTS.DTSName', 'LBUSv100')
    #uip.SetFieldValue('lperiod.period_code', '082013')
    #uip.SetFieldValue('lbranch.branch_code', '517001')
    #self.refDTSExit(self.panel1_lDTS)
    #self.refPeriodExit(self.panel1_lperiod)
    #self.refBranchExit(self.panel1_lbranch)
    self.FormContainer.Show()
  
  def refDTSExit(self, sender):
    sName = sender.Name
    DTSName = '%s.DTSName' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipart1.GetFieldValue(DTSName) == '-':
      self.uipart1.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "dts@lookupDTS", sName, 
        "DTSName;PeriodType;DTSId", None, {})
      self.CheckEntry()
      return res

  def refPeriodExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipart1.GetFieldValue("lperiod.period_code") == '-':
      self.uipart1.ClearLink("lperiod")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupPeriod", "lperiod", 
        "period_code;description;period_id", None, 
        {'period_type': self.uipart1.GetFieldValue("lDTS.PeriodType")})
      self.CheckEntry()
      return res

  def refBranchExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipart1.GetFieldValue("lbranch.branch_code") == '-':
      self.uipart1.ClearLink("lbranch")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupBranch", "lbranch", 
        "branch_code;branch_name;branch_id")
      self.CheckEntry()
      return res
      
  def RefreshGrid(self):
    app = self.FormObject.ClientApplication
    grid = self.uipart2
    uip = self.uipart1
    dtsid = self.uipart1.GetFieldValue("lDTS.DTSId")
    periodid = self.uipart1.GetFieldValue("lperiod.period_id")
    branchid =  self.uipart1.GetFieldValue("lbranch.branch_id") 
    bCode = self.uipart1.GetFieldValue("lbranch.branch_code")
    pCode = self.uipart1.GetFieldValue("lperiod.period_code")
    ph = app.CreateValues(['dtsid', dtsid], ['periodid', periodid], ['branchid', branchid], ['bCode', bCode], ['pCode', pCode])
    res = self.FormObject.CallServerMethod('GetGridData', ph)
    status = res.FirstRecord
    if status.Err!='':
      app.ShowMessage('Server Error : %s' % status.Err)
      return 0
    grid.ClearData()
    gData = res.Packet.gdata
    for i in range(gData.RecordCount):
      grid.Append()
      rec = gData.GetRecord(i)
      grid.formCode = rec.fkode
      grid.reportName = rec.fname
      grid.reportStatus = rec.status
    grid.First()     
    return 1 
    
  def CheckEntry(self):
    if self.uipart1.GetFieldValue("lperiod.period_id") not in (None,'') and self.uipart1.GetFieldValue("lbranch.branch_id") not in (None,'') and self.uipart1.GetFieldValue("lDTS.DTSId") not in (None, ''):
      self.RefreshGrid()
      return
    else:
      return
      
  def CallPengelolaan(self):
    app = self.FormObject.ClientApplication
    uip = self.uipart1
    st = self.uipart2.GetFieldValue('reportStatus')
    if st !='B':
      app.ShowMessage('Fungsi pengelolaan hanya dapat digunakan untuk form yang belum terisi')
      return
    frm = app.CreateForm('XBRL/fReportEditor', 'XBRL/fReportEditor', 2, None, None)
    fapp = frm.FormObject.ClientApplication
    frm.Show()
    fuip = frm.uipMain
    fuip.SetFieldValue('lDTS.DTSName', uip.GetFieldValue('lDTS.DTSName'))
    fuip.SetFieldValue('lReport.DTSFormCode', self.uipart2.GetFieldValue('formCode'))
    fuip.SetFieldValue('lperiod.period_code', uip.GetFieldValue('lperiod.period_code'))
    fuip.SetFieldValue('lbranch.branch_code', uip.GetFieldValue('lbranch.branch_code'))
    frm.refDTSExit(frm.pNav_lDTS)
    frm.refReportExit(frm.pNav_lReport)
    frm.refPeriodExit(frm.pNav_lperiod)
    frm.refBranchExit(frm.pNav_lbranch)
    frm.pNav_lDTS.Enabled = False
    frm.pNav_lReport.Enabled = False
    frm.pNav_lperiod.Enabled = False
    frm.pNav_lbranch.Enabled = False
    frm.bOpenOnClick(frm.pNav_bOpen)
    frm.pNav_bOpen.Enabled = False
    pass



  def button1OnClick(self, sender):
    # procedure(sender: TrtfButton)
    self.CheckEntry()
    pass