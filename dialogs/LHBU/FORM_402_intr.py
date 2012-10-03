REFMAP = {
  'LJENIS'                      : 'R_JENIS_PDN'
  ,'LVALUTA'                     : 'R_SANDI_VALUTA'
}
  
class LHBU_FORM_402:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LVALUTA'
    ]
    self.attrlist = [
      'Volume'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form402.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LVALUTA_reference_code'
        , 3: 'Volume'
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
    