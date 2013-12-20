class fAddTaxonomy:
  def __init__(self, formObj, parentForm):
    pass
  #--
  
  def Show(self):
    self.uipMain.periodetype = 'M'
    self.uipMain.procFlag = 1
    cb1 = self.FormObject.GetPanelByName('panel1').GetControlByName('cbProcess')
    cb1.Checked = True
    self.FormContainer.Show()

  def bBrowseOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipMain
    uip.Edit()
    uip.pathName = None
    app = self.FormObject.ClientApplication
    fname = app.OpenFileDialog('Import File', 'Zipped Taxonomy File (*.zip)|*.zip')
    if fname in (None,'',0):
      return
    x = app.CheckFileExist(fname)
    #app.ShowMessage(str(x))
    if x<1:
      app.ShowMessage('File %s tidak ditemukan.' % fname)
      return
      
    uip.pathName = fname
    if uip.dtsName in (None, ''):
      uip.dtsName = fname.split('\\')[-1].split('.zip')[0]
    uip.Post()
    


  def bUploadOnClick(self, sender):
    # procedure(sender: TrtfButton)
    uip = self.uipMain
    app = self.FormObject.ClientApplication
    
    if uip.pathName in (None,'',0):
      app.ShowMessage('Harap pilih file terlebih dahulu.')
      return
      
    if uip.dtsName in (None,'',0):
      app.ShowMessage('Nama DTS harus diisi.')
      return

    fname = uip.pathName
    if uip.procFlag==0:
      processFlag = False
    else:
      processFlag = True
    
    ph = app.CreateValues(['periode', uip.periodetype],['processFlag', processFlag])
    
    swfile = ph.Packet.AddStreamWrapper()
    swfile.LoadFromFile(fname)
    swfile.Name = uip.dtsName
    
    res = self.FormObject.CallServerMethod('ProsesDTS', ph)
    status = res.FirstRecord
    if status.ErrMessage not in (None,''):
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
    foundForm = res.packet.fList
    grid = self.uipDTS
    grid.ClearData()
    grid1 = self.FormObject.GetPanelByName('grid1')
    grid1.Caption = 'DTS Content [Found {0} form(s)]'.format(str(foundForm.RecordCount))
    
    for i in range(foundForm.RecordCount):
      grid.Append()
      rec = foundForm.GetRecord(i)
      grid.formCode = rec.kode
      grid.formName = rec.nama
      grid.formProcess = rec.proc
    
    grid.First()
    app.ShowMessage('File Successfully Uploaded.\nServer process time : {0} seconds'.format(str(status.ProcTime)))
    sender.Enabled = False
    
    #sender.ExitAction = 0

  def cbProcessOnClick(self, sender):
    # procedure(sender: TrtfCheckBox)
    self.uipMain.Edit()
    if sender.Checked:
      self.uipMain.procFlag = 1
    else:
      self.uipMain.procFlag = 0


  def button1OnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    grid1 = self.FormObject.GetPanelByName('grid1')
    ph = app.CreatePacket()
    #res = self.FormObject.CallServerMethod('test', ph)
    st = res.FirstRecord
    app.ShowMessage(str(st.tm))
    app.ShowMessage(grid1.Caption)
    pass