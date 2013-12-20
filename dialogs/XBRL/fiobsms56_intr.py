class fiobsms56:
  def __init__(self, formObj, parentForm):
    pass
  #--
  def Show(self):
    self.FormContainer.Show()
    
  def bGetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    filename = app.SaveFileDialog('Save data file','XLSX File|*.xlsx')
    if filename in (None,'',0):
      return
    filename = filename.rstrip('.xlsx') + '.xlsx'
    ph = app.CreateValues()
    ph = self.FormObject.CallServerMethod('GetData', ph)
    status = ph.FirstRecord
    if status.Err not in (None,'',0):
      app.ShowMessage('Server Error : ' % status.Err)
      return
    sw = ph.packet.GetStreamWrapper(0)
    sw.SaveToFile(filename)
    app.ShowMessage('File %s saved.' % filename)
    pass

  def bSetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    filename = app.OpenFileDialog('Open data file', 'XLSX File|*.xlsx')
    if filename in (None,'',0):
      return
    filename = filename.rstrip('.xlsx') + '.xlsx'
    if not app.ConfirmDialog('Anda yakin akan upload file %s ?\nSeluruh data pada database akan direplace.' % filename):
      return
    ph = app.CreateValues()
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(filename)
    ph = self.FormObject.CallServerMethod('SetData', ph)
    status = ph.FirstRecord
    if status.Err not in (None,'',0):
      app.ShowMessage('Server Error : ' % status.Err)
      return
    app.ShowMessage('File %s uploaded.' % filename)
    clicker = self.panel1_bView
    self.bViewOnClick(clicker)
    pass

  def bViewOnClick(self, sender):
    # procedure(sender: TrtfButton)
    m1 = 'View Existing Data Rekening'
    m2 = 'View Existing Data Agunan'
    l1 = 'Data Rekening'
    l2 = 'Data Agunan'
    app = self.FormObject.ClientApplication
    tbl = 'tmp_ls10'
    ldata = self.panel2_label1
    if sender.Caption == m2:
      tbl = 'tmp_ls10_agunan'
      sender.Caption = m1
      ldata.Caption = l2
    else:
      sender.Caption = m2
      ldata.Caption = l1
    ph = app.CreateValues(['tbl',tbl])
    self.FormObject.SetDataWithParameters(ph) 
    pass

  def FormAfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    if datapacket.FirstRecord not in (None,'',0):
      self.query1.SetDirectResponse(datapacket)
    pass

  def csvGetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    filename = app.SaveFileDialog('Save data file','ZIP File|*.zip')
    if filename in (None,'',0):
      return
    filename = filename.rstrip('.zip') + '.zip'
    ph = app.CreateValues()
    ph = self.FormObject.CallServerMethod('GetCSVData', ph)
    status = ph.FirstRecord
    if status.Err not in (None,'',0):
      app.ShowMessage('Server Error : ' % status.Err)
      return
    sw = ph.packet.GetStreamWrapper(0)
    sw.SaveToFile(filename)
    app.ShowMessage('File %s saved.' % filename)
    pass


  def csvSetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    app = self.FormObject.ClientApplication
    filename = app.OpenFileDialog('Open data file', 'ZIP File|*.zip')
    if filename in (None,'',0):
      return
    filename = filename.rstrip('.zip') + '.zip'
    if not app.ConfirmDialog('Anda yakin akan upload file %s ?\nSeluruh data pada database akan direplace.' % filename):
      return
    ph = app.CreateValues()
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(filename)
    ph = self.FormObject.CallServerMethod('SetCSVData', ph)
    status = ph.FirstRecord
    if status.Err not in (None,'',0):
      app.ShowMessage('Server Error : ' % status.Err)
      return
    app.ShowMessage('File %s uploaded.' % filename)
    clicker = self.panel1_bView
    self.bViewOnClick(clicker)
    pass
