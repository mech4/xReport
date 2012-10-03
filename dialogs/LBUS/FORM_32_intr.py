REFMAP = {
  'LGOLSTAT'     : 'R_SANDI_PIHAK_KETIGA'
 , 'LHUBBANK'      : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_32:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LGOLSTAT'
      ,'LHUBBANK'
    ]
    self.attrlist = ['Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form32.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LGOLSTAT_reference_code'
        , 2: 'LHUBBANK_reference_code'
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
    