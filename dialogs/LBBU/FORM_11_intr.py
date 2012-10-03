REFMAP = {
}
  
class LBBU_FORM_11:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
    ]
    self.attrlist = [
      'usd'
      ,'gbp'
      ,'sgd'
      ,'hkd'
      ,'jpy'
      ,'aud'
      ,'euro'
      ,'myr'
      ,'others'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form11.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'Aktivitas'
        , 2: 'usd'
        , 3: 'gbp'
        , 4: 'sgd'
        , 5: 'hkd'
        , 6: 'jpy'
        , 7: 'aud'
        , 8: 'euro'
        , 9: 'myr'
        , 10: 'others'
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
    