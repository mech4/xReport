REFMAP = {
  'LJANGKA'                     : 'R_JANGKA_WAKTU'
}
  
class LHBU_FORM_604:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJANGKA'
    ]
    self.attrlist = [
      'Realisasi'
      ,'Nisbah'
      ,'Distribusi'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form604.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJANGKA_reference_code'
        , 2: 'Realisasi'
        , 3: 'Nisbah'
        , 4: 'Distribusi'
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
    