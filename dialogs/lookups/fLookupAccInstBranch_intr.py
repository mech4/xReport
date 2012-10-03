class frmLookup:
  def __init__(self, formObject, parentForm):
    self.sPrefix = None
    self.sAccountCode = None
    
  def lookup(self, accountCode, codePrefix):
    formObj = self.FormObject
    app = formObj.ClientApplication
    bNeedRefresh = (self.sAccountCode != accountCode) or (self.sPrefix != codePrefix):
    if bNeedRefresh:
      ph = formObj.CallServerMethod("initQuery", app.CreateValues(['account_code', accountCode], ['prefix', codePrefix]))
      self.qLookup.SetDirectResponse(ph.packet)
      self.sPrefix = codePrefix
    #--
    res = self.FormContainer.Show()
    if res == 1:
      return self.qLookup.GetFieldValue('kode_cabang')
    else:
      return None
  #--
#--      