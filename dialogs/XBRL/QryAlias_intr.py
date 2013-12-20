class QryAlias:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self):
    self.FormContainer.Show()
    
  def FormAfterProcessServerData(self, formobj, operationid, datapacket):
    # function(formobj: TrtfForm; operationid: integer; datapacket: TPClassUIDataPacket):boolean
    app = formobj.ClientApplication
    dtype = {0 : 'unknown', 1 : 'string', 2 : 'integer', 3 : 'float', 4 : 'datetime', 5 : 'dataset'}
    rpt = ''
    if datapacket.FirstRecord not in (None,'',0):
      for i in range(datapacket.Definition.StructureDefCount):
        rpt+=str(datapacket.Definition.GetStructureDef(i).StructureName)
        rpt+='\n'
        for j in range(datapacket.Definition.GetStructureDef(i).FieldCount):
          fld = datapacket.Definition.GetStructureDef(i).GetFieldDef(j)
          rpt+='  {0} : {1}({2}) \n'.format(fld.FieldName,dtype[fld.DataType],fld.DataLength)
        rpt+='--------------------------\n'
      #app.ShowMessage(rpt)
      self.query1.SetDirectResponse(datapacket)
    pass
