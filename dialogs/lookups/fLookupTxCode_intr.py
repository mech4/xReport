class frmLookupTxCode:
  def __init__(self, formObject, parentForm):
    self.sPrefix = None
    
  def lookup(self, codePrefix):
    formObj = self.FormObject
    app = formObj.ClientApplication
    bNeedRefresh = self.sPrefix != codePrefix
    if bNeedRefresh:
      ph = formObj.CallServerMethod("initQuery", app.CreateValues(['prefix', codePrefix]))
      self.qLookup.SetDirectResponse(ph.packet)
      self.sPrefix = codePrefix
    #--
    res = self.FormContainer.Show()
    if res == 1:
      return self.qLookup.GetFieldValue('tx_code')
    else:
      return None
  #--
#--      