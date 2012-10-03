REFMAP = {
  'LBENTUKPENYISIHAN'           : 'R_BENTUK_PENYISIHAN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_13:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LBENTUKPENYISIHAN'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'CadKhususPPAP'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form13.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LBENTUKPENYISIHAN_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'CadUmumPPAP'
        , 4: 'CadKhususPPAP'
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
    