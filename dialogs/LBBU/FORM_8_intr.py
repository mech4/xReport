REFMAP = {
  'LJANGKA'                     : 'R_JANGKA_LBBU'
}
  
class LBBU_FORM_8:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJANGKA'
    ]
    self.attrlist = [
      'ImbalanDIM'
      ,'BagHas'
      ,'DistribusiDIM'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form8.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'PosisiDIM'
        , 2: 'LJANGKA_reference_code'
        , 3: 'ImbalanDIM'
        , 4: 'BagHas'
        , 5: 'DistribusiDIM'
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
    