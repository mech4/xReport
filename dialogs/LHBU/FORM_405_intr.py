REFMAP = {
  'LKOMPONEN'                   : 'R_KOMPONEN_RP'
}
  
class LHBU_FORM_405:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKOMPONEN'
    ]
    self.attrlist = [
      'Hari1'
      ,'Hari2'
      ,'Hari3'
      ,'Hari4'
      ,'Hari5'
      ,'Hari6'
      ,'Hari7'
      ,'Hari8'
      ,'Hari9'
      ,'Hari10'
      ,'Hari11'
      ,'Hari12'
      ,'Hari13'
      ,'Hari14'
      ,'Minggu3'
      ,'Minggu4'
      ,'sdbulan'
    ]
    self.paction     = None
    self.xlstemplate = 'lhbu/form405.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LKOMPONEN_reference_code'
        , 2: 'Hari1'
        , 3: 'Hari2'
        , 4: 'Hari3'
        , 5: 'Hari4'
        , 6: 'Hari5'
        , 7: 'Hari6'
        , 8: 'Hari7'
        , 9: 'Hari8'
        , 10: 'Hari9'
        , 11: 'Hari10'
        , 12: 'Hari11'
        , 13: 'Hari12'
        , 14: 'Hari13'
        , 15: 'Hari14'
        , 16: 'Minggu3'
        , 17: 'Minggu4'
        , 18: 'sdbulan'
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
    