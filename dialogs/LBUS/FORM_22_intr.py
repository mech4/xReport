REFMAP = {
  'LJENIS'                      : 'R_JENIS_SURAT_BERHARGA'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPEMBELI'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_22:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPEMBELI'
      ,'LHUBBANK'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'Persen'
      ,'Nominal'
      ,'Jumlah'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form22.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLPEMBELI_reference_code'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'Mulai'
        , 6: 'JatuhTempo'
        , 7: 'Persen'
        , 8: 'Nominal'
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
    