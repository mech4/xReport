REFMAP = {
  'LJenis'                      : 'R_JENIS_DANA'
}
  
class LBBU_FORM_3:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJenis'
    ]
    self.attrlist = [
      'PPKPKNVa'
      ,'PPDKRp'
      ,'PPDKVa'
      ,'PPDLRp'
      ,'PPDLVa'
      ,'PPSubJml'
      ,'PPSubJmlVa'
      ,'PDT1Rp'
      ,'PDT1Va'
      ,'PDT2Rp'
      ,'PDT2Va'
      ,'PDSubJmlRp'
      ,'PDSubJmlVa'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form3.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LJenis_reference_code'
        , 2: 'PPKPKNRp'
        , 3: 'PPKPKNVa'
        , 4: 'PPDKRp'
        , 5: 'PPDKVa'
        , 6: 'PPDLRp'
        , 7: 'PPDLVa'
        , 8: 'PPSubJml'
        , 9: 'PPSubJmlVa'
        , 10: 'PDT1Rp'
        , 11: 'PDT1Va'
        , 12: 'PDT2Rp'
        , 13: 'PDT2Va'
        , 14: 'PDSubJmlRp'
        , 15: 'PDSubJmlVa'
        , 16: 'Jumlah'
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
    