class fFormEditor:
  def __init__(self, formObj, parentForm):
    pass
  #--
  
  def Show(self):
    #lowerPart = self.GetPanelByName()
    uForm = self.uipForm
    fFlag = uForm.IsEmpty
    app = self.FormObject.ClientApplication
    FObj = self.FormObject
    uStatus = self.uipDetail
    uStatus.Edit()
    uStatus.SetFieldValue('fieldLoaded', 0)
    uStatus.Post()
    entitiesContainer = self.FormObject.PyFormObject.formFields
    # for test mode
    entitiesContainer.Visible = False
    if fFlag == 'T':
      # for test mode
      ##uField = self.uipField
      ##uField.Append()
      ##uField.fieldLevel = 0
      ##uField.fieldCode = 'TST'
      ##uField.fieldDesc = 'This is row test'
      ##uField.Post()
      pDetail = self.FormObject.GetPanelByName('pDetail')
      fType = pDetail.GetControlByName('FormType') 
      mType = pDetail.GetControlByName('mapType')
      fType.Enabled = False
      mType.Enabled = False
      bLoad = pDetail.GetControlByName('bLoad')
      bLoad.Enabled = False
    if uForm.GetFieldValue('mapType') == 'A':
      self.pDetail_bQuery.Enabled = True
    self.FormContainer.Show()
    
  def LoadFieldStructure(self):
    uStatus = self.uipDetail
    ffLoadStatus = uStatus.fieldLoaded
    if ffLoadStatus > 0:
      return 1
    app = self.FormObject.ClientApplication
    FObj = self.FormObject
    uForm = self.uipForm
    oldmap = uForm.OldMapType
    newmap = uForm.mapType
    oldsize = uForm.oldDataSize
    newsize = uForm.DataSize
    tempchange = 0
    if oldmap not in (None, '') and oldmap!=newmap:
      tempchange = 1      
    #if oldsize not in (None, '') and oldsize!=newsize:
    #  tempchange = 1      
    if self.pDetail_cb1.Checked:
      tempchange = 1
    formId = uForm.DTSFormId
    formType = uForm.FormType
    ph = app.CreateValues(['formId', formId],['formType', formType],['tempChange', tempchange],['dataSize',newsize])
    res = FObj.CallServerMethod('LoadStructure', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return
    tempLoc = status.tempLoc
    packet = res.Packet
    fData = packet.formFields
    grid = self.uipField
    grid.ClearData()
    for i in range(fData.RecordCount):
      grid.Append()
      rec = fData.GetRecord(i)
      grid.fieldLevel = rec.lv
      grid.fieldCode = rec.kode
      grid.fieldDesc = rec.desc
    grid.First()
    uStatus.Edit()
    uStatus.SetFieldValue('fieldLoaded', 1)
    uStatus.Post()
    uForm.Edit()
    uForm.SetFieldValue('tempLoc', tempLoc)
    uForm.Post()

  def IsEmptyOnChange(self, sender):
    # procedure(sender: TrtfDBComboBox)
    uip = self.uipForm
    if sender.ItemIndex == 0:
      entitiesContainer = self.FormObject.PyFormObject.formFields
      entitiesContainer.Visible = False
      pDetail = self.FormObject.GetPanelByName('pDetail')
      fType = pDetail.GetControlByName('FormType') 
      mType = pDetail.GetControlByName('mapType')
      bLoad = pDetail.GetControlByName('bLoad')
      bLoad.Enabled = False
      fType.Enabled = False
      mType.Enabled = False
      uip.FormType = 'N'
      uip.mapType = 'M'
    else:
      pDetail = self.FormObject.GetPanelByName('pDetail')
      fType = pDetail.GetControlByName('FormType') 
      mType = pDetail.GetControlByName('mapType')
      bLoad = pDetail.GetControlByName('bLoad')
      bLoad.Enabled = True
      fType.Enabled = True
      mType.Enabled = True
    #if uip.changed == 'F':
    #  uip.SetFieldValue('changed', 'T')

  def bLoadOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipForm
    fType = uip.FormType
    if fType in (None,'',0):
      app.ShowMessage('Form Type undefined.\nPlease choose Form Type before continue.')
      return
    self.LoadFieldStructure()
    entitiesContainer = self.FormObject.PyFormObject.formFields
    entitiesContainer.Visible = True

  def editQuery(self, sender):
    uip = self.uipForm
    grid = self.uipField
    app = self.FormObject.ClientApplication
    #if uip.changed == 'T':
    #  app.ShowMessage('Setting telah berubah, harap simpan dahulu sebelum melanjutkan.')
    #  return
    if uip.mapType == 'M':
      app.ShowMessage('Mapping manual tidak memiliki query, silahkan set mapping type menjadi automatic sebelum melanjutkan.')
      return
    if uip.FormType == 'N':
      app.ShowMessage('Form nihil tidak memiliki query, silahkan set ulang form type sebelum melanjutkan.')
      return
    if uip.tempLoc in (None,'',0):
      app.ShowMessage('Lokasi query belum terdefinisi, silahkan "Load Form Structure" terlebih dahulu.')
      return
    fid = uip.DTSFormId
    fName = uip.DTSFormCode
    tempLoc = uip.tempLoc
    fieldNum = grid.RecordCount
    ph = app.CreateValues(['fid', fid], ['fName', fName], ['tempLoc', tempLoc], ['fieldNum', fieldNum])
    frm = app.CreateForm('XBRL/fQueryEditor', 'XBRL/fQueryEditor', 2, ph, None)
    frm.Show()
    
  def FormTypeOnChange(self, sender):
    # procedure(sender: TrtfDBComboBox)
    uip = self.uipForm
    #if uip.changed == 'F':
    #  uip.Edit()
    #  uip.SetFieldValue('changed', 'T')
    #  uip.Post()
    pass

  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipForm
    app = self.FormObject.ClientApplication
    #if uip.changed == 'T':
    #  uip.Edit()
    #  uip.SetFieldValue('changed', 'F')
    #  uip.Post()
    formId = uip.DTSFormId
    isEmpty = uip.IsEmpty
    formType = uip.FormType
    dataSize = uip.DataSize
    if formType in (None,'',0):
      app.ShowMessage('Form Type undefined.\nPlease choose Form Type before continue.')
      return
    self.LoadFieldStructure()
    entitiesContainer = self.FormObject.PyFormObject.formFields
    entitiesContainer.Visible = True
    ph = app.CreateValues(['formId', formId],
                          ['isEmpty', isEmpty],
                          ['formType', formType],
                          ['dataSize', dataSize]
    )
    res = self.FormObject.CallServerMethod('SaveSetting', ph)
    status = res.FirstRecord
    if status.Is_Err != '':
      app.ShowMessage('Server Error : {0}'.format(status.Is_Err))
      return

    app.ShowMessage('Form setting saved.')


  def mapTypeOnChange(self, sender):
    # procedure(sender: TrtfDBComboBox)
    app = self.FormObject.ClientApplication
    editButton = self.pDetail_bQuery
    if sender.ItemIndex==0:
      editButton.Enabled = True
    else:
      editButton.Enabled = False
    pass

  def bCancelOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    return 1
