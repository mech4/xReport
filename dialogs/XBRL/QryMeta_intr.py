class QryMeta:
  def __init__(self, formObj, parentForm):
    pass
  #--
  
  def Show(self):
    uip = self.uipart1
    if uip.fid not in (None,'',0):
      self.panel1.Caption = 'FORM : '+uip.fName
    self.FormContainer.Show()
    pass
    
  def FormAfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    if datapacket.FirstRecord not in (None,'',0):
      #app.ShowMessage(str(datapacket))
      self.query1.SetDirectResponse(datapacket)
    pass

