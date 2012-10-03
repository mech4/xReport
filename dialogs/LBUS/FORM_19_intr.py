REFMAP = {
  'LJENIS'                      : 'R_JENIS_INV_TIDAK_TERIKAT'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPEMILIK'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LLOKASI'                     : 'R_DATI_2'
}
  
class LBUS_FORM_19:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPEMILIK'
      ,'LHUBBANK'
      ,'LLOKASI'
    ]
    self.attrlist = [
      'Bulan'
      ,'Hari'
      ,'Nisbah'
      ,'Persen'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form19.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'JumlahRekening'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'LGOLPEMILIK_reference_code'
        , 5: 'LHUBBANK_reference_code'
        , 6: 'LLOKASI_reference_code'
        , 7: 'Bulan'
        , 8: 'Hari'
        , 9: 'Nisbah'
        , 10: 'Persen'
        , 11: 'Jumlah'
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
    