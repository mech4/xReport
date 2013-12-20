class fQueryEditor:
  def __init__(self, formObj, parentForm):
    self.state = 0
    pass
  #--

  def Show(self):
    #qStr = self.FormObject.GetPanelByName('pMain').GetControlByName('QueryString')
    IsNew = self.uipQuery.GetFieldValue('IsNew')
    bSave = self.FormObject.GetPanelByName('pMain').GetControlByName('bSave')
    bSave.Enabled = False 
    if IsNew not in (None,'',0,'T'):
      self.state = 2
      self.LoadExistingQuery()
    else:
      self.state = 1
    self.CheckState()
    self.FormContainer.Show()
  
  def bBrowseOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    qryContainer = self.pEditor_qryEditor
    filename = app.OpenFileDialog('Import Data', 'Text Document (*.txt)|*.txt')
    if filename not in (None,'',0):
      iTxt = open(filename, 'r')
      qryTxt = iTxt.read()
      iTxt.close()
      qryContainer.Text = qryTxt
      qryContainer.Enabled = True
      bSave = self.FormObject.GetPanelByName('pMain').GetControlByName('bSave')
      bSave.Enabled = True 
      bLoad = self.FormObject.GetPanelByName('pMain').GetControlByName('bOpen')
      bLoad.Enabled = False
    pass

  def bOpenOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    qryContainer = self.pEditor_qryEditor
    qryContainer.Enabled = True
    if self.state == 1:
      qryContainer.Text = ''
    bSave = self.FormObject.GetPanelByName('pMain').GetControlByName('bSave')
    bSave.Enabled = True 
    qryContainer.SetFocus()
    sender.Enabled = False
    pass

  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    qryContainer = self.pEditor_qryEditor
    qryText = qryContainer.Text
    if qryText in (None, ''):
      app.ShowMessage('Cannot save empty query')
      return
    uip = self.uipQuery
    fid = uip.dtsformid or 0
    mid = uip.DTSMapId or 0
    qid = uip.qid or 0
    tempLoc = uip.QueryString
    fieldNum = uip.fieldNum
    ph = app.CreateValues(['qryText', qryText],['fid',fid],['mid',mid],['qid',qid],['tempLoc',tempLoc],['fieldNum',fieldNum])
    ret = self.FormObject.CallServerMethod('saveQry', ph)
    status = ret.FirstRecord
    if status.ErrMessage not in (None,'',0):
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
    app.ShowMessage('Query successfully saved')
    qryContainer.Enabled = False
    bSave = self.FormObject.GetPanelByName('pMain').GetControlByName('bSave')
    bSave.Enabled = False 
    bLoad = self.FormObject.GetPanelByName('pMain').GetControlByName('bOpen')
    bLoad.Enabled = True
    bLoad.Caption = '&Edit'
    uip.Edit()
    uip.SetFieldValue('qid', status.qid)
    uip.SetFieldValue('DTSMapId', status.mid)
    uip.Post()
    self.state = 2
    self.CheckState()
    pass
    
  def LoadExistingQuery(self):
    app = self.FormObject.ClientApplication
    tempLoc = self.uipQuery.GetFieldValue('QueryString')
    ph = app.CreateValues(['tempLoc',tempLoc])
    res = self.FormObject.CallServerMethod('LoadQueryFromFile', ph)
    status = res.FirstRecord
    if status.ErrMessage != '':
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
      
    if status.qryText == '':
      app.ShowMessage('Error : query file is empty')
      return
      
    qryContainer = self.pEditor_qryEditor
    qryContainer.Text = status.qryText
    pass
  
  def CheckState(self):
    bLoad = self.FormObject.GetPanelByName('pMain').GetControlByName('bOpen')
    bDel = self.FormObject.GetPanelByName('pMain').GetControlByName('bDelete')
    if self.state == 1:
      bLoad.Caption = '&New'
      bDel.Enabled = False
    elif self.state == 2:
      bLoad.Caption = '&Edit'
      bDel.Enabled = True
    else:
      pass

  def bDeleteOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    if not app.ConfirmDialog('Menghapus query berarti merubah jenis mapping menjadi manual.\nAnda yakin akan melanjutkan ?'):
      return
    qryContainer = self.pEditor_qryEditor
    uip = self.uipQuery
    fid = uip.dtsformid or 0
    mid = uip.DTSMapId or 0
    qid = uip.qid or 0
    tempLoc = uip.QueryString
    ph = app.CreateValues(['fid',fid],['mid',mid],['qid',qid],['tempLoc',tempLoc])
    ret = self.FormObject.CallServerMethod('deleteQry', ph)
    status = ret.FirstRecord
    if status.ErrMessage not in (None,'',0):
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
    qryContainer.Text = ''
    sender.Enabled = False
    uip.Edit()
    uip.SetFieldValue('DTSMapId', None)
    uip.SetFieldValue('qid', None)
    uip.Post()
    self.state = 1
    self.CheckState()
    pass

    
  def bEnumOnClick(self, sender):
    uip = self.uipQuery
    app = self.FormObject.ClientApplication
    dtsid = uip.GetFieldValue('dtsid')
    fid = uip.GetFieldValue('dtsformid')
    ph = app.CreateValues(['dtsid', dtsid],['fid',fid])
    frm = app.CreateForm('XBRL/QryEnum', 'XBRL/QryEnum', 2, ph, None)
    frm.Show()
    


  def bStructOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipQuery
    app = self.FormObject.ClientApplication
    fName = uip.GetFieldValue('AssignCode')
    fid = uip.GetFieldValue('dtsformid')
    ph = app.CreateValues(['fName', fName],['fid',fid])
    frm = app.CreateForm('XBRL/QryMeta', 'XBRL/QryMeta', 2, ph, None)
    frm.Show()
    pass