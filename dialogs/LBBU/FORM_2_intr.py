REFMAP = {
  'LPos'                        : 'R_POS2_LBBU'
}
  
class LBBU_FORM_2:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LPos'
    ]
    self.attrlist = [
      'PPRupiah'
      ,'PPValas'
      ,'PPJumlah'
      ,'PLRupiah'
      ,'PLValas'
      ,'PLJumlah'
      ,'BPRupiah'
      ,'BPValas'
      ,'BPJumlah'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form2.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'No'
        , 2: 'LPos_reference_code'
        , 3: 'PPRupiah'
        , 4: 'PPValas'
        , 5: 'PPJumlah'
        , 6: 'PLRupiah'
        , 7: 'PLValas'
        , 8: 'PLJumlah'
        , 9: 'BPRupiah'
        , 10: 'BPValas'
        , 11: 'BPJumlah'
        , 12: 'Jumlah'
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
    