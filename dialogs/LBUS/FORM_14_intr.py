REFMAP = {
  'LTUJUAN'                     : 'R_TUJUAN_ISTISHNA'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPRODUSEN'                : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LMETODE'                     : 'R_PENGAKUAN_PENDAPATAN'
}
  
class LBUS_FORM_14:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LTUJUAN'
      ,'LJENISVALUTA'
      ,'LGOLPRODUSEN'
      ,'LHUBBANK'
      ,'LMETODE'
    ]
    self.attrlist = [
      'Mulai'
      ,'JatuhTempo'
      ,'HargaKontrak'
      ,'PersenPenyelesaian'
      ,'Termin'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form14.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'NomorRekening'
        , 2: 'LTUJUAN_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'LGOLPRODUSEN_reference_code'
        , 5: 'LHUBBANK_reference_code'
        , 6: 'Mulai'
        , 7: 'JatuhTempo'
        , 8: 'HargaKontrak'
        , 9: 'PersenPenyelesaian'
        , 10: 'LMETODE_reference_code'
        , 11: 'Termin'
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
    