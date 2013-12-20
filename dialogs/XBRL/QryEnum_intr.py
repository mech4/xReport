class QryEnum:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self):
    app = self.FormObject.ClientApplication
    dtsid = self.uipart1.dtsid
    fid = self.uipart1.fid
    enumIndex = self.uipart1.enumIndex
    res = self.FormObject.CallServerMethod('GetEnumNames', app.CreateValues(['dtsid',dtsid],['fid',fid]))
    status = res.FirstRecord
    if status.Err != '':
      app.ShowMessage('Error : %s' % status.Err)
      return
    eList = res.Packet.eList
    strList = ''
    for i in range(eList.RecordCount):
      rec = eList.GetRecord(i)
      if i>0:
        strList += '\n'
      strList += rec.item 
    cbList = self.FormObject.GetPanelByName('panel1').GetControlByName('Test')
    #app.ShowMessage(strList)
    cbList.Items = strList  
    cbList.Values = strList  
    if self.uipart1.StateName != 'edit':
      self.uipart1.Edit()
    cbList.ItemIndex = enumIndex
    #self.query1.Refresh()
    self.FormContainer.Show()
    self.FormObject.GetPanelByName('panel1').GetControlByName('button1').SetFocus()
    #self.FormObject.GetPanelByName('query1').SetFocus
    #o = self.FormObject.GetPanelByName('query1').FieldCount
    #app.ShowMessage(str(o))
    
  def FormAfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    if datapacket.FirstRecord not in (None,'',0):
      #app.ShowMessage(str(datapacket))
      self.query1.SetDirectResponse(datapacket)
    pass

  def TestOnChange(self, sender):
    # procedure(sender: TrtfDBComboBox)
    items = sender.Items.split('\n')
    uip = self.uipart1
    dtsid = uip.dtsid
    enumname = items[sender.ItemIndex]
    iIndex = sender.ItemIndex 
    app = self.FormObject.ClientApplication
    if uip.fid>0:
      fid = uip.fid
      ph = app.CreateValues(['dtsid', dtsid], ['enumname', enumname], ['iIndex', iIndex], ['fid', fid])
    else:
      ph = app.CreateValues(['dtsid', dtsid], ['enumname', enumname], ['iIndex', iIndex])
    self.FormObject.SetDataWithParameters(ph)
    self.Show()
    

  def FormOnClose(self, formobj):
    # procedure(formobj: TrtfForm)
    self.FormObject.GetPanelByName('panel1').GetControlByName('button1').SetFocus()
    pass