REFMAP = {
}
  
class LBUS_FORM_41:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
    ]
    self.attrlist = [
      'Uraian'
      ,'Jumlah'
      ,'No'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form41.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'No'
        , 2: 'Uraian'
        , 3: 'Jumlah'
    }
  #--

  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
    else:  
      res = uapp.stdLookup(sender, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
        
      return res
  def onEnter(self, sender):
    uipData = self.uipData
    uipData.Edit()
    uipData.Uraian = self.pData_eUraian.Text

    