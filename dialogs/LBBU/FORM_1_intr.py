REFMAP = {
}
  
class LBBU_FORM_1:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
    ]
    self.attrlist = [
      'Rupiah'
      ,'Valas'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form1.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'Tanggal'
        , 2: 'Rupiah'
        , 3: 'Valas'
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
    