REFMAP = {
  'LSIFAT'                      : 'R_SIFAT_SIMPANAN_WADIAH'
  ,'LJENIS'                      : 'R_JENIS_SIMPANAN_WADIAH'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPEMILIK'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LLOKASI'                     : 'R_DATI_2'
}
  
class LBUS_FORM_18:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSIFAT'
      ,'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPEMILIK'
      ,'LHUBBANK'
      ,'LLOKASI'
    ]
    self.attrlist = [
      'PersenBonus'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form18.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'JumlahRekening'
        , 2: 'LSIFAT_reference_code'
        , 3: 'LJENIS_reference_code'
        , 4: 'LJENISVALUTA_reference_code'
        , 5: 'LGOLPEMILIK_reference_code'
        , 6: 'LHUBBANK_reference_code'
        , 7: 'LLOKASI_reference_code'
        , 8: 'PersenBonus'
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
    