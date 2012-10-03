REFMAP = {
  'LJENISOPERASIONAL'           : 'R_JENIS_OPERASIONAL'
  ,'LJENIS'                      : 'R_JENIS_AKTIVA_DI_INDONES'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_15:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENISOPERASIONAL'
      ,'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form15.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJENISOPERASIONAL_reference_code'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'Jumlah'
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
    