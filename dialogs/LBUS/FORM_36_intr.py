REFMAP = {
  'LJENIS'                     : 'R_PIUTANG_PEMBIAYAAN'
  , 'LJENISVALUTA'             : 'R_JENIS_VALUTA'
  , 'LBENTUKPENGHAPUSANBUKUAN' : 'R_BENTUK_HAPUS_BUKU'
  , 'LDEBITUR'                 : 'R_SANDI_BANK'
  , 'LHUBUNGANBANK'            : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LKOLEKTIBILITAS'           : 'R_KOLEKTIBILITAS'
}
  
class LBUS_FORM_03:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LBENTUKPENGHAPUSANBUKUAN'
      ,'LJENISVALUTA'
      ,'LDEBITUR'
      ,'LHUBUNGANBANK'
      ,'LKOLEKTIBILITAS'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'TanggalHapusBuku'
      ,'Agunan'
      ,'BakiDebetHapusbuku'
      ,'BakiDebetBulan'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form36.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'NoRekening'
        , 2: 'JumlahRekening'
        , 3: 'LJENIS_reference_code'
        , 4: 'LBENTUKPENGHAPUSANBUKUAN_reference_code'
        , 5: 'LJENISVALUTA_reference_code'
        , 6: 'LDEBITUR_reference_code'
        , 7: 'LHUBUNGANBANK_reference_code'
        , 8: 'TanggalHapusBuku'
        , 9: 'LKOLEKTIBILITAS_reference_code'
        , 10: 'Agunan'
        , 11: 'BakiDebetHapusbuku'
        , 12: 'BakiDebetBulan'
        , 13: 'Jumlah'
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
    