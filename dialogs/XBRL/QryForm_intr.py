class QryForm:
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
    
  def ProcData(self, params):
    # after dev this function is unused
    rec = params.FirstRecord
    dtsformid = rec.dtsformid
    dtsformcode = rec.dtsformcode 
    uip = self.uipMain
    dtsid = uip.GetFieldValue('dtsid')
    app = self.FormObject.ClientApplication
    #app.ShowMessage('{0} {1}'.format(dtsformid,dtsid))
    #app.ShowMessage(str(dtsformid))
    ph = app.CreateValues(['dtsformid',dtsformid],['dtsformcode',dtsformcode],['dtsid', dtsid])
    res = self.FormObject.CallServerMethod('PrepareForm', ph)
    status = res.FirstRecord
    if status.ErrMessage not in (None,''):
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
    #app.ShowMessage('%s.xls created.' % dtsformcode)
    return

  def setEmpty(self, params):
    #change to empty form only
    rec = params.FirstRecord
    dtsformid = rec.dtsformid
    dtsformcode = rec.dtsformcode 
    uip = self.uipMain
    dtsid = uip.GetFieldValue('dtsid')
    app = self.FormObject.ClientApplication
    if not app.ConfirmDialog('Anda yakin form %s akan diset sebagai form nihil ?' % str(dtsformcode)):
      return
    ph = app.CreateValues(['dtsformid',dtsformid],['dtsformcode',dtsformcode],['dtsid', dtsid])
    res = self.FormObject.CallServerMethod('PrepareEmptyForm', ph)
    status = res.FirstRecord
    if status.ErrMessage not in (None,''):
      app.ShowMessage('Error : %s' % status.ErrMessage)
      return
    return
