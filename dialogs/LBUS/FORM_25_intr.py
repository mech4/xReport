REFMAP = {
  'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLKREDITUR'                : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_25:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENISVALUTA'
      ,'LGOLKREDITUR'
      ,'LHUBBANK'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'Persen'
      ,'Jumlah'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form25.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENISVALUTA_reference_code'
        , 2: 'LGOLKREDITUR_reference_code'
        , 3: 'LHUBBANK_reference_code'
        , 4: 'Mulai'
        , 5: 'JatuhTempo'
        , 6: 'Persen'
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
    