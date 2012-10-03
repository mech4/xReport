REFMAP = {
  'LJENIS'                      : 'R_JENIS_KEWAJIBAN_PADA_BI'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_20:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'Hari'
      ,'Persen'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form20.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'Bulan'
        , 4: 'Hari'
        , 5: 'Persen'
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
    