REFMAP = {
    'LJENISDEVIRATIF' : ''
  , 'LJENISOPTION'    : ''
  , 'LVALUTADASAR'    : 'R_JENIS_VALUTA'
  , 'LVALUTALAWAN'    : 'R_JENIS_VALUTA'
  , 'LSTATUSPEMBELI'  : 'R_STATUS_PEMBELI'
  , 'LSANDIPEMBELI'   : 'R_STATUS_PEMBELI'
  , 'LSANDIPEMBELINONBANK' :''
  , 'LSTATUSPENJUAL'  : 'R_STATUS_PEMBELI'
  , 'LSANDIPENJUAL'   : 'R_STATUS_PEMBELI'
  , 'LSANDIPENJUALNONBANK' : '
  , 'LTUJUAN' : 'R_SANDI_TUJUAN'
  , 'LSANDINEGARAPEMBELI' : 'R_SANDI_NEGARA'
  , 'LSANDINEGARAPENJUAL' : 'R_SANDI_NEGARA'

}
  
class LHBU_FORM_202:
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
    