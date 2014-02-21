# GLOBAL VARS
xl_filename = ''

class fReportEditor:
  def __init__(self, formObj, parentForm):
    pass
  #--
  def Show(self):
    self.FormContainer.Show()
  
  def PrepareTemp(self):
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    pCode = uip.GetFieldValue("lperiod.period_code")
    period_id = uip.GetFieldValue("lperiod.period_id")
    branch_id = uip.GetFieldValue("lbranch.branch_id")
    ph = app.CreateValues(['DTSFormId', DTSFormId],['DTSFileName', DTSFileName],['DTSId', DTSId],['period_id', period_id],['pCode', pCode],['branch_id',branch_id])
    res = self.FormObject.CallServerMethod('PrepareTemp', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return
    
  def refDTSExit(self, sender):
    sName = sender.Name
    DTSName = '%s.DTSName' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue(DTSName) == '-':
      self.uipMain.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "dts@lookupDTS", sName, 
        "DTSName;PeriodType;DTSId", None, {})
        
      return res

  def refPeriodExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("lperiod.period_code") == '-':
      self.uipMain.ClearLink("lperiod")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupPeriod", "lperiod", 
        "period_code;description;period_id", None, 
        {'period_type': self.uipMain.GetFieldValue("lDTS.PeriodType")})
      return res

  def refBranchExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue("lbranch.branch_code") == '-':
      self.uipMain.ClearLink("lbranch")
      return 1
    else:  
      res = uapp.stdLookup(sender, "report@lookupBranch", "lbranch", 
        "branch_code;branch_name;branch_id")
      return res

  def refReportExit(self, sender):
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    pNav = self.FormObject.GetPanelByName('pNav')
    bOpen = pNav.GetControlByName('bOpen')
    bSave = pNav.GetControlByName('bSave')
    if DTSId in (None, '', 0):
      app.ShowMessage('Harap pilih DTS terlebih dahulu.')
      return 1
    sName = sender.Name
    DTSName = '%s.DTSFormCode' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipMain.GetFieldValue(DTSName) == '-':
      self.uipMain.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "dts@lookupReport", sName, 
        "DTSFormCode;DTSFormDesc;DTSFormId;DTSFolderId;DTSFileName;FormType;IsEmpty;DataSize", None, 
        {'DTSFormCode' : self.uipMain.GetFieldValue(DTSName) or '', 'DTSId' : DTSId})
      uip.SetFieldValue('fType', uip.GetFieldValue('lReport.FormType'))
      if uip.GetFieldValue('lReport.IsEmpty') == 'T':
        bOpen.Enabled = False
        bSave.Enabled = False
      else:
        bOpen.Enabled = True
        bSave.Enabled = True
      #app.ShowMessage(str(res))
      return res

  def refExit(self, sender):
    pass

  def bOpenOnClick(self, sender):
    # procedure(sender: TrtfButton)
    global xl_filename
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    pCode = uip.GetFieldValue("lperiod.period_code")
    period_id = uip.GetFieldValue("lperiod.period_id")
    branch_id = uip.GetFieldValue("lbranch.branch_id")
    if DTSFormId in (None, '', 0):
      app.ShowMessage('Harap pilih report form terlebih dahulu.')
      return 1
    recflag = 0
    if self.pNav_cb1.Checked:
      if app.ConfirmDialog('Anda yakin akan membuat ulang template ?'):
        recflag = 1
      else:
        return 1
    self.PrepareTemp()
    ph = app.CreateValues(
        ['DTSFormId', DTSFormId],
        ['DTSFileName', DTSFileName],
        ['DTSId', DTSId],
        ['period_id', period_id],
        ['pCode', pCode],
        ['branch_id',branch_id], 
        ['recflag', recflag]
    )
    res = self.FormObject.CallServerMethod('OpenReport', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return
    packet = res.Packet
    if packet.StreamWrapperCount > 0:
      sw = packet.GetStreamWrapper(0)
    else:
      raise Exception, 'PERINGATAN!. Download stream not found'

    tmp_filename = app.GetTemporaryFileName("dl")
    xl_filename = tmp_filename + '.xlsx'
    sw.SaveToFile(xl_filename)

    oc = self.FormObject.GetPanelByName('xbrli')
    #olecont.CreateObjectFromFile(localfile)
    oc.CreateObjectFromFile(xl_filename)
    pLog = self.FormObject.GetPanelByName('pLog')
    lMemo = pLog.GetControlByName('logMemo')
    lMemo.Text = ''

  
  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    global xl_filename
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    pCode = uip.GetFieldValue("lperiod.period_code")
    period_id = uip.GetFieldValue("lperiod.period_id")
    branch_id = uip.GetFieldValue("lbranch.branch_id")
    oc = self.FormObject.GetPanelByName('xbrli')
    #olecont.CreateObjectFromFile(localfile)
    #oc.SaveAsDocument(xl_filename)
    oc.OLEObject.ActiveDocument.SaveAs(xl_filename)
    if DTSFormId in (None, '', 0):
      app.ShowMessage('Harap pilih report form terlebih dahulu.')
      return 1
    ph = app.CreateValues(['DTSFormId', DTSFormId],['DTSFileName', DTSFileName],['DTSId', DTSId],['period_id', period_id],['pCode', pCode],['branch_id',branch_id])
    sw = ph.Packet.AddStreamWrapper()
    #sw.LoadFromFile(localfile)
    sw.LoadFromFile(xl_filename)
    res = self.FormObject.CallServerMethod('SaveReport', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return
    app.ShowMessage('Data {0} telah tersimpan.'.format(uip.GetFieldValue('lReport.DTSFormCode')))
    return 1

  def bGenOnClickAsli(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    if DTSFormId in (None, '', 0):
      app.ShowMessage('Harap pilih report form terlebih dahulu.')
      return 1
    ph = app.CreateValues(['DTSFormId', DTSFormId],['DTSFileName', DTSFileName],['DTSId', DTSId])
    res = self.FormObject.CallServerMethod('GenReport', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return

  def bGenOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    DTSFormCode = uip.GetFieldValue('lReport.DTSFormCode') 
    FormType = uip.GetFieldValue('lReport.FormType') 
    IsEmpty = uip.GetFieldValue('lReport.IsEmpty') 
    dataSize = uip.GetFieldValue('lReport.DataSize')
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    pCode = uip.GetFieldValue("lperiod.period_code")
    period_id = uip.GetFieldValue("lperiod.period_id")
    bCode = uip.GetFieldValue("lbranch.branch_code")
    branch_id = uip.GetFieldValue("lbranch.branch_id")
    pLog = self.FormObject.GetPanelByName('pLog')
    lMemo = pLog.GetControlByName('logMemo')
    if IsEmpty != 'T':
      self.PrepareTemp()
      #oc = self.FormObject.GetPanelByName('xbrli')
      #olecont.CreateObjectFromFile(localfile)
      #oc.SaveAsDocument(xl_filename)
    if DTSFormId in (None, '', 0):
      app.ShowMessage('Harap pilih report form terlebih dahulu.')
      return 1
    ph = app.CreateValues(['DTSFormId', DTSFormId],
                          ['DTSFileName', DTSFileName],
                          ['DTSFormCode', DTSFormCode],
                          ['DTSId', DTSId],
                          ['period_id', period_id],
                          ['branch_id', branch_id],
                          ['bCode', bCode],
                          ['pCode', pCode],
                          ['FormType', FormType],
                          ['IsEmpty', IsEmpty],
                          ['dataSize', dataSize]
    )
    if xl_filename in (None,'',0) and uip.GetFieldValue('lReport.IsEmpty') != 'T':
      app.ShowMessage('Harap buka report terlebih dahulu dengan menggunakan tombol Open.')
      return 1
    if IsEmpty != 'T':
      sw = ph.Packet.AddStreamWrapper()
      #sw.LoadFromFile(localfile)
      sw.LoadFromFile(xl_filename)
    res = self.FormObject.CallServerMethod('GenReport', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      if status.is_valid != '':
        app.ShowMessage('Tidak lolos validasi bisnis.\nPeriksa log untuk detail kesalahan.')
        lMemo.Text = 'Tidak lolos validasi\r\n--------------------\r\n{0}'.format(status.Is_Err)
      else:
        app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
        lMemo.Text = 'Server Error : {0}'.format(status.Is_Err) 
      return
    packet = res.packet
    if packet.StreamWrapperCount > 0:
      sw = packet.GetStreamWrapper(0)
    else:
      lMemo.Text = 'PERINGATAN!. Download stream not found' 
      raise Exception, 'PERINGATAN!. Download stream not found'
    sFileName = 'c:\\{0}'.format(status.fName)  
    sw.SaveToFile(sFileName)
    app.ShowMessage('Instance successfully saved as {0}'.format(sFileName))    
    lMemo.Text = 'Instance successfully saved as {0}'.format(sFileName) 

  def bTestOnClick(self, sender):
    # procedure(sender: TrtfButton)
    global xl_filename
    app = self.FormObject.ClientApplication
    oc = self.FormObject.GetPanelByName('xbrli')
    oc.SetFocus()
    app.ShowMessage(xl_filename)

  def bGetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    global xl_filename
    app = self.FormObject.ClientApplication
    if xl_filename in (0,'',None):
      app.ShowMessage('Harap buka file terlebih dahulu.')
      return 1
    ph = app.CreatePacket()
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(xl_filename)
    dl_filename = app.SaveFileDialog('Save As Document', 'Excel 2007 XLSX (*.xlsx)| *.xlsx')
    if dl_filename in (0,'',None):
      return 1
    dl_filename = dl_filename.rstrip('.xlsx') + '.xlsx'
    sw.SaveToFile(dl_filename)
    app.ShowMessage('Successfully saved as {0}'.format(dl_filename)) 
    pass

  def bSetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    uip = self.uipMain
    DTSId = uip.GetFieldValue('lDTS.DTSId') 
    DTSFormId = uip.GetFieldValue('lReport.DTSFormId') 
    period_id = uip.GetFieldValue("lperiod.period_id")
    branch_id = uip.GetFieldValue("lbranch.branch_id")
    if DTSFormId in (None, '', 0) or period_id in (None, '', 0)  or branch_id in (None, '', 0):
      app.ShowMessage('Harap pilih report form terlebih dahulu.')
      return 1
    ul_filename = app.OpenFileDialog('Choose File to Upload', 'Excel 2007 XLSX (*.xlsx)| *.xlsx')
    if ul_filename in (0,'',None):
      return 1
    DTSFileName = uip.GetFieldValue('lReport.DTSFileName') 
    pCode = uip.GetFieldValue("lperiod.period_code")
    ph = app.CreateValues(['DTSFormId', DTSFormId],['DTSFileName', DTSFileName],['DTSId', DTSId],['period_id', period_id],['pCode', pCode],['branch_id',branch_id])
    sw = ph.Packet.AddStreamWrapper()
    #sw.LoadFromFile(localfile)
    sw.LoadFromFile(ul_filename)
    res = self.FormObject.CallServerMethod('SaveReport', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return
    app.ShowMessage('Data {0} telah tersimpan.'.format(uip.GetFieldValue('lReport.DTSFormCode')))
    return 1
    pass
    