REFMAP = {
  'LPOS'                        : 'R_POS_NERACA'
}
  
class LBBU_FORM_4B:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPOS'
    ]
    self.attrlist = [
      'Eks1'
      ,'Eks3'
      ,'Eks6'
      ,'Eks12'
      ,'Eks15'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form4B.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LPOS_reference_code'
        , 2: 'Saldo'
        , 3: 'Eks1'
        , 4: 'Eks3'
        , 5: 'Eks6'
        , 6: 'Eks12'
        , 7: 'Eks15'
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
    