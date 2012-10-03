class record: pass

class Application:
  def __init__(self, dafApp):
    # we control async tasks by storing their request IDs in global application object
    # after async task is completed, the request id is set to None 
    self.asyncTaskDemo_RID = None
    self.dafApp = dafApp
    
    # other initialization here
    self.loadedForms = {} # dictionary with formName: formObject pairs
    self.loadedresources = []
    self.openfunctions   = {}
    self.systemTxCodes = {}
    
    clientAttrUtilClass = dafApp.GetClientClass("clientattrutil", "ClientAttrUtil")
    self.clientAttrUtil = clientAttrUtilClass()
    #--
    pass
  #--
  
  def checkLoadedForm(self, formID):
    return self.loadedForms.get(formID, None)
    
  def registerForm(self, formID, formObject):
    if self.loadedForms.get(formID) != None:
      raise Exception, "Form already registered %s" % formID
    else:
      self.loadedForms[formID] = formObject
      return formObject
    #--
  #--
  
  def unregisterForm(self, formID):
    if self.loadedForms.get(formID) != None:
      del self.loadedForms[formID]
    #--
  #--
  
  def clearLoadedForms(self):
    self.loadedForms.clear()
    
  def stdLookup(self, comboControl, serverLookupID, linkElmtName, displayFields, addParamFieldNames = None, dParameterValues = {}):
    # simplified interface to lookup method
    # linkElmtName: link element name (string)
    # displayFields: list of key (inputed) and displayed fields (string), separated with ";" character. key field must appear first
    # addParamFieldNames: list of field names for additional parameters (string), separated with ";"
    #   note: parameters in form linkname.fieldname will be translated into fieldname, unless a name conflict occurs
    #         the key field will always be a parameter with key field name as parameter
    ownerForm = comboControl.OwnerForm
    systemContext = ownerForm.SystemContext
    if systemContext != "":
      form_id = "%s://lookups/fGenLookup" % systemContext
    else:
      form_id = "lookups/fGenLookup"
    lookupForm = self.checkLoadedForm(form_id)
    if lookupForm == None:
      lookupForm = self.dafApp.CreateForm(form_id, "lookups.fGenLookup", 0, None, None)
      self.registerForm(form_id, lookupForm)
    #--
    return lookupForm.stdLookup(comboControl, serverLookupID, linkElmtName, displayFields, addParamFieldNames, dParameterValues) 
    
  def lookupCustomer(self):
    lookupForm = self.checkLoadedForm("lookups.fSelectCustomer")
    if lookupForm == None:
      lookupForm = self.dafApp.CreateForm("lookups/fSelectCustomer", "lookups.fSelectCustomer", 0, None, None)
      self.registerForm("lookups.fSelectCustomer", lookupForm)
    #--
    return lookupForm.getCustomer()
  #--
  
  def getDateTuple(self, aDate):
    mlu = self.dafApp.ModDateTime
    if type(aDate) is list or type(aDate) is tuple:
      return (aDate[0], aDate[1], aDate[2])
    else:
      elmts = mlu.DecodeDate(aDate)
      return (elmts[0], elmts[1], elmts[2])
    #--
  #--
    
  def stdDate(self, aDate):
    datelib = self.dafApp.ModDateTime
    if type(aDate) is list or type(aDate) is tuple:
      return datelib.EncodeDate(aDate[0], aDate[1], aDate[2])
    else:
      return aDate
    #--
  #--
  
  def selectCustomer(self):
    frm = self.checkLoadedForm('fSelectCustomer')
    if frm == None:
      frm = self.dafApp.CreateForm('fSelectCustomer', 'fSelectCustomer', 0, None, None)
      self.registerForm('fSelectCustomer', frm)
    return frm.getCustomer()
  #--
  
  def addSystemTxCode(self, tx_code, is_reserved, remote_form_id, subsystem_code, is_local, session_name):
    dEntry = {'is_reserved': is_reserved, 'remote_form_id': remote_form_id, 'is_local': is_local, 'session_name': session_name} 
    self.systemTxCodes[tx_code] = dEntry 
    return dEntry
  
  def checkSystemTxCode(self, tx_code):
    return self.systemTxCodes.get(tx_code, None)
  #--
  
#-- class Application
    
def OnAsyncTaskTermination(app, requestID, bError, errMessage, scriptResult):
  appObject = app.UserAppObject
  if appObject.asyncTaskDemo_RID == requestID:
    appObject.asyncTaskDemo_RID = None
    if not bError:
      rec = scriptResult.FirstRecord
      app.ShowMessage("Task is completed successfully: %d" % rec.loop_passed)
    else:
      app.ShowMessage("Task was completed with error\r\n%s" % errMessage)
  #--
#--

def OnLogout(app):
    return app.ConfirmDialog('Anda yakin untuk logout?')  