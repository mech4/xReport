REFMAP = {
  'LKANTOR'                     : 'R_SANDI_KANTOR'
  ,'LJENIS'                      : 'R_JENIS_AKTIVA_DI_INDONES'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_16:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKANTOR'
      ,'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'Bulan'
      ,'Hari'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form16.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LKANTOR_reference_code'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'PersenBagiHasil'
        , 5: 'Bulan'
        , 6: 'Hari'
        , 7: 'Jumlah'
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
    