REFMAP = {
  'LJENIS'           : 'R_JENIS_SIMPANAN_WADIAH'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'Bulan'
      , 'Hari'
      , 'PersentaseBonus'
      , 'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form03.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'
      , 2: 'LJENISVALUTA_reference_code'
      , 3: 'Bulan'
      , 4: 'Hari'
      , 5: 'PersentaseBonus'
      , 6: 'Jumlah'
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
    