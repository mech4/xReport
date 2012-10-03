REFMAP = {
  'LSANDIBANK'                     : 'R_SANDI_BANK'
  , 'LTRANSDERIVATIF'              : 'R_DERIVATIF_VALAS'
  , 'LTRANSDERIVATIFASING'         : 'R_DERIVATIF_BUKAN_ASING'
}
  
class LBUS_FORM_204:
  def __init__(self, formObj, parentForm):
    pass
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
    