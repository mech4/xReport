REFMAP = {
  'LGOLPEMSAH'     : 'R_GOL_PEMEGANG_SAHAM'

}
  
class LBUS_FORM_31:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LGOLPEMSAH'
    ]
    self.attrlist = ['Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form31.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLPEMSAH_reference_code'
        , 2: 'Jumlah'
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
    