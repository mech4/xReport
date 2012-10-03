class frmLookup:
  def __init__(self, formObject, parentForm):
    self.dParameters = {}
    self.lookupID = ""
    self.bHasQueryResult = False
    
  def checkSamePrevParameter(self, dParameterValues):
    for key in dParameterValues.keys():
      if self.dParameters.get(key, None) != dParameterValues[key]:
        return False
    return True
  
  def getServerParameters(self, lookupID, dParameterValues):
    formObj = self.FormObject
    app = formObj.ClientApplication
    ph = app.CreatePacket()
    fieldNamesAndTypes = ['lookup_id: string']
    for key in dParameterValues.keys():
      val = dParameterValues[key]
      if val == None:
        raise Exception, "Lookup parameter value %s cannot be None" % str(key)
      if type(val) is str:
        tName = 'string'
      elif type(val) is int:
        tName = 'integer'
      elif type(val) is float:
        tName = 'float'
      else:
        raise Exception, "Unsupported data type for lookup parameter value %s: %s" % (str(key), str(type(val)))
      #--
      pair = "%s: %s" % (str(key), tName)
      #app.ShowMessage('pair = ' + pair)
      fieldNamesAndTypes.append(pair)
    #--
    sDecl = ";".join(fieldNamesAndTypes)
    rec = ph.packet.CreateDataPacketStructure(sDecl)
    
    rec.lookup_id = lookupID
    for key in dParameterValues.keys():
      rec.SetFieldByName(str(key), dParameterValues[key])
    return ph
  #--
   
  def completeParameters(self, uipData, paramFieldNames, dParameterValues):
    newParams = {}
    for key in dParameterValues.keys():
      newParams[key] = dParameterValues[key]
      
    for paramField in paramFieldNames:
      splits = paramField.split("@", 1)
      if len(splits) == 1:
        paramField = splits[0] 
        keyName = splits[0]
      else:
        paramField = splits[0]
        keyName = splits[1]
      #--
        
      fieldValue = uipData.GetFieldValue(paramField)
      if fieldValue == None:
        fieldValue = ''
      newParams[keyName] = fieldValue
      #self.FormObject.ShowMessage('params[%s]=%s' % (keyName, fieldValue))
    #--
    return newParams
    
  def transferValues(self, uipData, uiFieldMap):
    uipData.ForceEdit()
    for uipField in uiFieldMap.keys():
      qFieldName = uiFieldMap[uipField]
      uipData.SetFieldValue(uipField, self.qLookup.GetFieldValue(qFieldName))
    #--
  #--
    
  def stdLookup(self, comboControl, serverLookupID, linkElmtName, displayFields, addParamFieldNames = None, dParameterValues = {}):
    # simplified interface to lookup method
    # linkElmtName: link element name (string)
    # displayFields: list of key (inputed) and displayed fields (string), separated with ";" character. key field must appear first
    # addParamFieldNames: list of field names for additional parameters (string), separated with ";"
    #   note: parameters in form linkname.fieldname will be translated into fieldname, unless a name conflict occurs
    #         the key field will always be a parameter with key field name as parameter
    if displayFields.strip() == "":
      raise Exception, "stdLookup(): displayFields cannot be empty"
    if linkElmtName.strip() == "":
      raise Exception, "stdLookup(): linkElmtName cannot be empty"
    dispFields = displayFields.split(";")
    keyField = dispFields[0].lower()
    uiFieldMap = {}
    for dispField in dispFields:
      uiFieldName = "%s.%s" % (linkElmtName, dispField)
      uiFieldMap[uiFieldName] = dispField
    #--
    paramFieldNames = []
    paramFieldNames.append("%s.%s@%s" % (linkElmtName, keyField, keyField))
    currParamNames = {keyField: None}
    
    if addParamFieldNames != None:
      addParamFields = addParamFieldNames.split(";")
      for paramField in addParamFields:
        paramField = paramField.lower()
        iPos = paramField.find(".")
        bUseAltParam = False
        if iPos >= 0:
          altParamName = paramField[iPos + 1:]
          bUseAltParam = not currParamNames.has_key(altParamName) # no name conflict
        #--
        if not bUseAltParam:
          paramFieldNames.append(paramField)
          currParamNames[paramField] = None
        else:
          paramFieldNames.append("%s@%s" % (paramField, altParamName))
          currParamNames[altParamName] = None
        #--
      #-- for
    #--
    return self.lookup(comboControl, serverLookupID, uiFieldMap, paramFieldNames, dParameterValues)
  #-- stdLookup 
  
  def lookup(self, comboControl, lookupID, uiFieldMap, paramFieldNames, dParameterValues = {}):
    # comboControl: reference to rtfDBComboEdit
    # uiFieldMap: dictionary containing <uipField>: <queryField>
    # paramFieldNames: list or tuple of field names to be inclulded in parameter
    # dParameterValues: dictionary of misc parameter value 
    formObj = self.FormObject
    app = formObj.ClientApplication
    uipData = comboControl.owner.UIPart 
    dParameterValues = self.completeParameters(uipData, paramFieldNames, dParameterValues)
    bNoRefresh = self.bHasQueryResult and (lookupID == self.lookupID) and self.checkSamePrevParameter(dParameterValues)
    bShowLookup = True  
    if not bNoRefresh:
      #app.ShowMessage(str(dParameterValues))
      ph = self.getServerParameters(lookupID, dParameterValues)
      phRes = formObj.CallServerMethod("initQuery", ph)
      dsStatus = phRes.packet.status
      recStatus = dsStatus.GetRecord(0)
      if recStatus.isErr:
        raise Exception, recStatus.errMsg
      bTransferValues = False
      if recStatus.rowCount == 1: # is unique row
        comboControl.LookupValid = 1
        bShowLookup = False
        self.bHasQueryResult = False
        self.qLookup.SetDirectResponse(phRes.packet)
        bTransferValues = True
      elif recStatus.rowCount == 0: # row not found
        app.ShowMessage("Data not found")
        return 0 
      else:
        self.qLookup.SetDirectResponse(phRes.packet)
        bShowLookup = True
        bTransferValues = False
        self.bHasQueryResult = True
        comboControl.LookupSelected = 1
      #-- if recStatus
    #-- if not bNoRefresh
    self.lookupID = lookupID
    self.dParameters = dParameterValues
    if bShowLookup:
      res = self.FormContainer.Show()
      bTransferValues = res == 1
    #--
    if bTransferValues:
      self.transferValues(uipData, uiFieldMap)
      return 1
    else:
      return 0
  #--
#--      