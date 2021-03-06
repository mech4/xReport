# DEFS
ATTR_ORACLE   = 0x01
ATTR_MONGODB  = 0x02 
ATTR_TYPE     = ATTR_ORACLE  

class fReportContainer:
  def __init__(self, formObj, parentForm):
    self.repform     = None
    self.group_code  = None
    self.period_type = None
    self.NewData = 1
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
         ['group_code', group_code]
    )
    res = self.FormObject.CallServerMethod('PeriodHandler', ph)
    self.FormContainer.Show()
    self.switchEdit(False)
    self.uipMain.beginRow = 1
    self.uipMain.endRow = 100
    self.pData_endRow.enabled = 0
    self.pData_totalRow.enabled = 0
    if group_code == 'LBBU':
      self.pData_cbNihil.Visible=1
    else:
      self.pData_cbNihil.Visible=0
    
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
      form_no = self.uipMain.GetFieldValue('reportclass.report_code')
      if form_no==None : form_no=''
      if self.group_code=='LKPBU' and form_no=='FORM707':
        res = uapp.stdLookup(sender, "report@lookupPeriod", "period", 
          "period_code;description;period_id", None, 
          {'period_type': 'D', 'description' : 'Friday,'})
      else:
        res = uapp.stdLookup(sender, "report@lookupPeriod", "period", 
          "period_code;description;period_id", None, 
          {'period_type': self.period_type})
      if self.group_code=='LBBU' and (form_no[-1:] not in ('1','2','3') or form_no[-2:] in ('10','11')):
        week = self.uipMain.GetFieldValue('period.period_code')
        if week==None: week=''
        if week[-1:] in ('1','2','3'):
          self.uipMain.ClearLink("reportclass")  
      return res

  def reportOnExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("reportclass.report_code") == '-':
      self.uipMain.ClearLink("reportclass")
      return 1
    else:  
      week = self.uipMain.GetFieldValue('period.period_code')
      if week==None: week=''
      if week[-1:] in ('1','2','3') and self.group_code=='LBBU':
        res = uapp.stdLookup(sender, "report@lookupReportClass", "reportclass", 
          "report_code;report_name;class_id;form_id;periode_type", None, 
          {'group_code': self.group_code, 'periode_type': 'W'})
      else:
        res = uapp.stdLookup(sender, "report@lookupReportClass", "reportclass", 
          "report_code;report_name;class_id;form_id;periode_type", None, 
          {'group_code': self.group_code})
      if self.group_code=='LKPBU' and self.uipMain.GetFieldValue('reportclass.report_code')!='FORM707' and len(week)>6: 
        self.uipMain.ClearLink("period")
      if self.group_code=='LKPBU' and self.uipMain.GetFieldValue('reportclass.report_code')=='FORM707' and len(week)<7: 
        self.uipMain.ClearLink("period")
      self.period_type = self.uipMain.GetFieldValue('reportclass.periode_type')
      self.uipMain.ClearLink("period")
      #self.period_type = self.uipMain.GetFieldValue("reportclass.periode_type")
      #self.uipMain.ClearLink("period")
        
      return res

  def switchEdit(self, swOn=True):
    if self.repform != None:
      self.repform.pData.SetAllControlsReadOnly(not swOn)
      #pass
    self.pData_bSave.enabled = swOn
    self.pData_bDownload.enabled = swOn
    self.pData_bGenerate.enabled = swOn
    self.pData_bRecreate.enabled = swOn
    self.pData_bImport.enabled = swOn
    self.pAction_bSaveRow.enabled = swOn
    self.pAction_bNewrow.enabled = swOn
    self.pAction_bDeleteRow.enabled = swOn
    
  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    formobj = self.FormObject; app = formobj.ClientApplication
    if self.repform == None: return
    if self.pData_cbNihil.checked:
      if app.ConfirmDialog('Anda yakin %s pada periode %s diisi dengan nihil ?' % (
                 self.uipMain.GetFieldValue('reportclass.report_name'),
                 self.uipMain.GetFieldValue('period.description')
                 )):
        oldData = self.repform.uipData 
        oldData.First()
        item_id = oldData.item_id
        for i in range(oldData.RecordCount):
          self.uipDeleted.Append()
          self.uipDeleted.item_id = item_id
          self.uipDeleted.Post()
          oldData.Next()
          item_id = oldData.item_id
        self.repform.uipData.ClearData()

      else:
        self.pData_cbNihil.checked = 0
        return
    
    self.uipMain.Edit()
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
      self.pData_bDownload.enabled = 1
      self.pData_bGenerate.enabled = 1
      self.pData_bRecreate.enabled = 1
      self.pData_bSave.enabled = 1
      self.pData_bImport.enabled = 1
      self.pAction_bNewrow.enabled = 1
      self.pAction_bDeleteRow.enabled = 1
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
    try:
      check = self.repform.txttemplate
    except:
      self.repform.txttemplate = ''
      self.repform.txtmap = ()
      self.repform.useheader = None
    self.setAttrList()
    
    if  self.pData_cbAllData.checked == 0:
      beginRow = self.uipMain.beginRow or 1
      limitRow = 0
    else:
      beginRow = 1
      limitRow = 1
    ph = app.CreateValues(
      ["class_id", uipMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uipMain.GetFieldValue("period.period_id")]
      , ["branch_id", uipMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uipMain.GetFieldValue("reportclass.report_code")]
      , ["beginRow", beginRow]
      , ["limitRow", limitRow]
      , ["attrlist", str(self.load_attrlist)]
    )
    self.repform.FormObject.SetDataWithParameters(ph)
    
    if self.repform.paction not in (None,''):
      self.pData_cbNihil.enabled = 1
    else:
      self.pData_cbNihil.checked = 0
      self.pData_cbNihil.enabled = 0
    self.switchEdit()
    uMain = self.uipMain    
    ph = app.CreateValues(
      ["class_id", uMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uMain.GetFieldValue("period.period_id")]
      , ["branch_id", uMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uipMain.GetFieldValue("reportclass.report_code")]
    )
    ph = formObj.CallServerMethod('CheckRepExist', ph)
    status = ph.FirstRecord
    uMain.Edit()
    if  self.pData_cbAllData.checked == 0:
      uMain.endRow = uMain.beginRow + 99
      if uMain.endRow > status.totalRow:
        uMain.endRow = status.totalRow 
    else:
      uMain.beginRow = 1
      uMain.endRow = status.totalRow
    uMain.totalRow = status.totalRow
    uMain.Post()
    if status.IsErr == 1:
      uMain.Edit()
      uMain.endRow = self.repform.uipData.RecordCount
      uMain.totalRow = self.repform.uipData.RecordCount
      uMain.Post()
      self.pData_bDownload.enabled = 0
      self.pData_bGenerate.enabled = 0
      self.pData_bRecreate.enabled = 0
    #--


  def bNewRowOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.repform != None:
      self.repform.uipData.Append()
      self.switchEdit()
      self.repform.pData.GetControl(0).SetFocus()
    #--
    self.pAction_bSaveRow.enabled = 1

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
    self.pAction_bSaveRow.enabled = 1
    self.pData_bSave.enabled = 1

  def bSaveRowOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.repform != None:
      self.repform.uipData.Edit()
      self.repform.uipData.Post()
    #--
    self.pData_bSave.enabled = 1



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
    
    if self.repform.useheader > 10:
      ph = formobj.CallServerMethod('DownloadF707', ph)
    else:
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
    filename = ''
    
    uMain = self.uipMain
        
    if self.repform.useheader > 10:
      filename = app.SaveFileDialog("Simpan File CSV [Nama File Otomatis Sesuai Tanggal Laporan]", "CSV Files (*.csv)|*.csv")
      if filename in (None,'',0):
        return 
      if filename[-4:].lower() != '.csv':
        filename += '.csv'
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
      ph = formobj.CallServerMethod('GenerateF707', ph)
    else:
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
      if self.repform.useheader > 10:
        fname = filename.split('\\')[-1]
        filename = filename.split(fname)[0]+status.fname+'.csv'
        f = open(filename, "w")
        f.write(status.storeFile)
        f.close()
        app.ShowMessage("File %s telah tersimpan." % filename)
      else:
        oPrint = app.GetClientClass('PrintLib','PrintLib')()
        oPrint.doProcess(app, ph.packet, 1)    
    #--
    


  def bImportOnClick(self, sender):
    formobj = self.FormObject; app = formobj.ClientApplication
    if  self.pData_cbAllData.checked == 0 or self.uipMain.beginRow<>1 or self.uipMain.endRow<>self.uipMain.totalRow:
      app.ShowMessage('Harap pilih semua data dan load ulang form terlebih dahulu.')
      return
      
    filename = app.OpenFileDialog('Import Data', 'Excel Worksheet (*.xls)')
    if filename in (None,''):
      return
      
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
      , ["check1", uMain.GetFieldValue("reportclass.report_name")]
      , ["check2", uMain.GetFieldValue("branch.branch_code")+" - "+uMain.GetFieldValue("branch.branch_name")]
      , ["check3", uMain.GetFieldValue("period.period_code")+" - "+uMain.GetFieldValue("period.description")]
      , ["formid", uMain.GetFieldValue("reportclass.form_id")] 
    )
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(filename)
    sw.Name = filename.split('.')[0].split('\\')[-1]
    
    if self.repform.useheader > 10:
      ph = formobj.CallServerMethod('ImportF707', ph)
    else:
      ph = formobj.CallServerMethod('ImportReport', ph)
    
    status = ph.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    else:
      ds = ph.packet
      iData = ds.iData
      if str(self.repform.reflist) not in ('[]',):
        iLink = ds.iReff
      recnum = iData.RecordCount
      fieldnum = iData.Structure.FieldCount 
      sat = ''
      if recnum==0:
        app.ShowMessage("File Contains no Data.")
        return
      elif recnum==1:
        sat = 'Record'
      else:
        sat = 'Records'
      if app.ConfirmDialog("%d %s of Data Found.\nLoad Data into Form ?" % (recnum, sat)):
        #pcln = app.CreateValues(
        #  ["class_id", uMain.GetFieldValue("reportclass.class_id")]
        #  , ["period_id", uMain.GetFieldValue("period.period_id")]
        #  , ["branch_id", uMain.GetFieldValue("branch.branch_id")]
        #  , ["group_code", self.group_code]
        #  , ["report_code", uMain.GetFieldValue("reportclass.report_code")]
        #  , ["attrlist", str(self.load_attrlist)]
        #)
        #st = formobj.CallServerMethod('CleanThisForm', pcln)
        #status = st.FirstRecord
        #if status.IsErr == 1:
        #  app.ShowMessage("ERROR! " + status.ErrMessage)
        datamap = str(self.repform.xlsmap)
        datamap = eval(datamap)
        oldData = self.repform.uipData 
        oldData.First()
        item_id = oldData.item_id
        for i in range(oldData.RecordCount):
          self.uipDeleted.Append()
          self.uipDeleted.item_id = item_id
          self.uipDeleted.Post()
          oldData.Next()
          item_id = oldData.item_id
        self.repform.uipData.ClearData()
        putData = self.repform.uipData
        for i in range(recnum):
          rec = iData.GetRecord(i)
          if str(self.repform.reflist) not in ('[]',):
            rLink = iLink.GetRecord(i)
          putData.Append()
          for j in range(fieldnum):
            if datamap.values()[j][0] != '!':
              putData.SetFieldValue(iData.Structure.GetFieldDef(j).FieldName,
                                     rec.GetFieldByName(iData.Structure.GetFieldDef(j).FieldName)
              )
              if iData.Structure.GetFieldDef(j).FieldName.split('.')[0] in self.repform.reflist:
                putData.SetFieldValue(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".refdata_id",
                                      rLink.GetFieldByName(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".refdata_id")
                ) 
                putData.SetFieldValue(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".reference_desc",
                                      rLink.GetFieldByName(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".reference_desc")
                ) 
                putData.SetFieldValue(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".reference_code",
                                      rLink.GetFieldByName(iData.Structure.GetFieldDef(j).FieldName.split('.')[0]+".reference_code")
                ) 
        #self.bSaveOnClick(self.pData_bSave)
        self.uipMain.Edit()
        self.uipMain.beginRow = 1
        self.uipMain.endRow = recnum
        self.uipMain.totalRow = recnum
        self.uipMain.Post()
    #--
    
    

  def beginRowOnExit(self, sender):
    # procedure(sender: TrtfDBEdit)
    self.uipMain.endRow = self.uipMain.beginRow + 99
    

  def bRecreateOnClick(self, sender):
    # procedure(sender: TrtfButton)
    formObj = self.FormObject; app = formObj.ClientApplication
    uipMain = self.uipMain
    
    formid = uipMain.GetFieldValue("reportclass.form_id") or ''
    periodid = uipMain.GetFieldValue("period.period_id") or ''
    branchid = uipMain.GetFieldValue("branch.branch_id") or ''
    if formid == '' or periodid == '' or branchid == '':
      app.ShowMessage("Input not completed yet!")
      return
    ph = app.CreateValues(
      ["class_id", uipMain.GetFieldValue("reportclass.class_id")]
      , ["period_id", uipMain.GetFieldValue("period.period_id")]
      , ["branch_id", uipMain.GetFieldValue("branch.branch_id")]
      , ["group_code", self.group_code]
      , ["report_code", uipMain.GetFieldValue("reportclass.report_code")]
      , ["attrlist", str(self.load_attrlist)]
    )
    confirmed = app.ConfirmDialog('Anda yakin akan membuat ulang Form : %s' % uipMain.GetFieldValue("reportclass.report_name"))
    if not confirmed:
      self.bLoadOnClick(self.pData_bLoad)
      return

    st = formObj.CallServerMethod('CleanThisForm', ph)
    status = st.FirstRecord
    if status.IsErr == 1:
      app.ShowMessage("ERROR! " + status.ErrMessage)
    self.bLoadOnClick(self.pData_bLoad)
    #--


  def cbAllDataOnClick(self, sender):
    # procedure(sender: TrtfCheckBox)
    formObj = self.FormObject; app = formObj.ClientApplication
    uipMain = self.uipMain
    if sender.checked == 0:
      self.pData_beginRow.enabled = 1
      #self.pData_endRow.enabled = 1
      #self.pData_totalRow.enabled = 1
    else:
      self.pData_beginRow.enabled = 0
      self.pData_endRow.enabled = 0
      self.pData_totalRow.enabled = 0
    