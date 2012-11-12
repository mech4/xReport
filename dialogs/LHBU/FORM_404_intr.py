REFMAP = {
  'LPOS'                        : 'R_JENIS_POSPOS'
}
  
class LHBU_FORM_404:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPOS'
    ]
    self.attrlist = [
      'Rupiah'
      ,'Valas'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form404.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LPOS_reference_code'
        , 2: 'Rupiah'
        , 3: 'Valas'
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
    