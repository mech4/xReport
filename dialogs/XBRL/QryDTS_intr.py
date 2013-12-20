class QryDTS:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self):
    self.FormContainer.Show()
    
  def FormAfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    if datapacket.FirstRecord not in (None,'',0):
      #app.ShowMessage(str(datapacket))
      self.query1.SetDirectResponse(datapacket)
    pass
