REFMAP = {
    'LJENISDEVIRATIF' : 
  , 'LSTATUSCOUNTERPART' : '
  , 'LSANDICOUNTERPART'  :
  , 'LSANDICOUNTERPARTNONBANK' :
  , 'LTUJUAN' : 'R_SANDI_TUJUAN'
  , 'LMATAUANG' : 'R_SANDI_VALUTA'
  , 'LSANDINEGARACOUNTERPART' :

}
  
class LHBU_FORM_203:
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
    