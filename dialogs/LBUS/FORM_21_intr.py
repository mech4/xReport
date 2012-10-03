REFMAP = {
  'LBANK'                       : 'R_SANDI_BANK'
  ,'LJENISIOPERASIONAL'          : 'R_JENIS_OPERASIONAL'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LJENIS'                      : 'R_JENIS_KWJBN_BANK_LAIN'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
}
  
class LBUS_FORM_21:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LBANK'
      ,'LJENISIOPERASIONAL'
      ,'LHUBBANK'
      ,'LJENIS'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'Persen'
      ,'Jumlah'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form21.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LBANK_reference_code'
        , 2: 'LJENISIOPERASIONAL_reference_code'
        , 3: 'LHUBBANK_reference_code'
        , 4: 'LJENIS_reference_code'
        , 5: 'LJENISVALUTA_reference_code'
        , 6: 'Mulai'
        , 7: 'JatuhTempo'
        , 8: 'Persen'
        , 9: 'Jumlah'
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
    